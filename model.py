import os
import psycopg2
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error

# Connexion à PostgreSQL et récupération des données
connection = psycopg2.connect(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB")
)

query = "SELECT * FROM public.message_data"
df = pd.read_sql(query, connection)
connection.close()

# Préparation des données
# Suppression des lignes avec des valeurs manquantes dans la colonne cible 'grade'
df = df.dropna(subset=['grade'])

# Séparation des caractéristiques (features) et de la cible (target)
X = df.drop('grade', axis=1)
y = df['grade']

# Colonnes numériques et catégorielles
numeric_features = ['niv']
categorical_features = ['univ', 'course', 'session', 'anonymous', 'username', 'ville', 'pays', 'genre', 'annee_naissance', 'niveau_education']

# Préprocesseur
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

# Modèles de régression
models = {
    'LinearRegression': LinearRegression(),
    'RandomForestRegressor': RandomForestRegressor(),
    'SVR': SVR()
}

# Paramètres pour GridSearch
param_grids = {
    'LinearRegression': {},
    'RandomForestRegressor': {
        'model__n_estimators': [100, 200],
        'model__max_depth': [None, 10, 20]
    },
    'SVR': {
        'model__C': [0.1, 1, 10],
        'model__gamma': ['scale', 'auto']
    }
}

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

best_models = {}
for name, model in models.items():
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('model', model)])
    
    grid_search = GridSearchCV(pipeline, param_grid=param_grids[name], cv=5, n_jobs=-1, scoring='neg_mean_squared_error')
    grid_search.fit(X_train, y_train)
    best_models[name] = grid_search.best_estimator_
    print(f"Best parameters for {name}: {grid_search.best_params_}")
    print(f"Best score for {name}: {grid_search.best_score_}")

# Évaluation des modèles
for name, model in best_models.items():
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error for {name}: {mse}")
