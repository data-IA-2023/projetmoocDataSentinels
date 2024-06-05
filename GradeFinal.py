import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
from datetime import datetime
import mlflow
import mlflow.sklearn
from sqlalchemy import create_engine, inspect
import joblib
import psycopg2
import joblib
import os
import ast


connection = psycopg2.connect(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB")
)

query = """SELECT * 
           FROM public.combined_view 
           WHERE (grade IS NOT NULL)
           ;"""
           #AND (username IS NOT NULL) AND (course_id IS NOT NULL) AND (course IS NOT NULL) AND (gender IS NOT NULL) AND (year_of_birth IS NOT NULL) AND (csp IS NOT NULL) AND (level_of_education IS NOT NULL)
df = pd.read_sql(query, connection)
connection.close()

print(df)
print(df.dtypes)

def calculate_age(X):
    current_year = datetime.now().year
    return current_year - X

X = df[['course', 'bodyemotion', 'country', 'gender', 'year_of_birth', 'csp', 'level_of_education']]
y = df['grade'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numeric_features = ['year_of_birth']
categorical_features = ['course', 'bodyemotion', 'country', 'gender', 'csp', 'level_of_education']

# Numeric transformer
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('age_calculator', FunctionTransformer(calculate_age, validate=False)),
    ('scaler', StandardScaler())
])

# Categorical transformer
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')), 
    ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
])

# Combine all transformers into a single ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

mlflow.set_tracking_uri("file:./mlruns")

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    models = [
        # {
        #     "name": "DecisionTreeRegressor",
        #     "estimator": Pipeline(steps=[
        #         ('preprocessor', preprocessor), 
        #         ('regressor', DecisionTreeRegressor(random_state=42))
        #     ]),
        #     "param_grid": { 
        #         'regressor__max_depth': [3, 5, 7, None],
        #         'regressor__min_samples_split': [2, 5, 10],
        #         'regressor__min_samples_leaf': [1, 2, 4]
        #     } 
        # },
        {
            "name": "RandomForestRegressor",
            "estimator": Pipeline(steps=[
                ('preprocessor', preprocessor), 
                ('regressor', RandomForestRegressor(random_state=42))
            ]),
            "param_grid": { 
                'regressor__n_estimators': [50, 100, 200],
                'regressor__max_depth': [3, 5, 7, None],
                'regressor__min_samples_split': [2, 5, 10],
                'regressor__min_samples_leaf': [1, 2, 4]
            } 
        },
        # {
        #     "name": "Ridge",
        #     "estimator": Pipeline(steps=[
        #         ('preprocessor', preprocessor), 
        #         ('regressor', Ridge())
        #     ]),
        #     "param_grid": { 
        #         # 'regressor__alpha': [0.01, 0.1, 1, 10, 100]
        #         'regressor__alpha': [1]
        #     } 
        # },
    ]

    results = []

    for model_info in models:
        with mlflow.start_run(run_name=model_info['name']):
            grid_search = GridSearchCV(model_info['estimator'], model_info['param_grid'], n_jobs=12)
            grid_search.fit(X_train, y_train)

            best_params = grid_search.best_params_
            print(f"Best parameters for model {model_info['name']}: {best_params}")

            best_model = grid_search.best_estimator_

            y_pred = best_model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            mlflow.set_tag("model", model_info['name'])
            mlflow.log_params(best_params)
            mlflow.log_metrics({
                "mean_squared_error": mse,
                "r2_score": r2,
            })
            mlflow.sklearn.log_model(best_model, "model")

            # Sauvegarde du modèle avec joblib
            joblib.dump(best_model, f"{model_info['name']}_model.joblib")

            print(f"Mean Squared Error for {model_info['name']}: {mse}")
            results.append((model_info['name'], mse, r2))

    return results

results = train_and_evaluate_models(X_train, X_test, y_train, y_test)

print('Recuperation des performances des models:')
for model_name, mse, r2 in results:
    print(f"{model_name} - MSE: {mse}, R2: {r2}")

# Fonction pour charger un modèle sauvegardé et faire des prédictions
def load_model_and_predict(model_path, X_new):
    # Charger le modèle sauvegardé
    model = joblib.load(model_path)
    
    # Faire des prédictions
    predictions = model.predict(X_new)
    
    return predictions

# Exemple d'utilisation de la fonction de prédiction
# X_new est un DataFrame avec les nouvelles données
# predictions = load_model_and_predict("RandomForestRegressor_model.joblib", X_new)
