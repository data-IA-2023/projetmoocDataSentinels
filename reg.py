import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, GridSearchCV
from datetime import datetime
import mlflow
import mlflow.sklearn
import psycopg2
import joblib
import os
import ast

# Configuration de la connexion à la base de données
connection = psycopg2.connect(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB")
)

query = """SELECT * 
           FROM public.combined_view 
           WHERE grade IS NOT NULL  
           LIMIT 100;"""
df = pd.read_sql(query, connection)
connection.close()

# Convert the string representations of lists into actual lists
df['embedding'] = df['embedding'].apply(ast.literal_eval)

# Ensure all column names are strings
df.columns = df.columns.astype(str)

def calculate_age(X):
    current_year = datetime.now().year
    return current_year - X

def process_embedding(embeddings):
    return np.array(embeddings.values.tolist())

# Define features and target
X = df[['course', 'bodyemotion', 'country', 'gender', 'year_of_birth', 'csp', 'level_of_education', 'embedding']]
y = df['grade']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define numeric and categorical features
numeric_features = ['year_of_birth']
embedding_features = ['embedding']
categorical_features = ['course', 'bodyemotion', 'country', 'gender', 'csp', 'level_of_education']

# Numeric transformer
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('age_calculator', FunctionTransformer(calculate_age, validate=False)),
    ('scaler', StandardScaler())
])

# Embedding transformer
embedding_transformer = Pipeline(steps=[
    ('process', FunctionTransformer(process_embedding, validate=False))
])

# Categorical transformer
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop='first'))
])

# Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        # ('embed', embedding_transformer, embedding_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Set MLflow tracking URI
mlflow.set_tracking_uri("file:./mlruns")

# Train and evaluate models
def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    models = [
        {
            "name": "LinearRegression",
            "estimator": Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('svd', TruncatedSVD()),
                ('regressor', LinearRegression())
            ]),
            "param_grid": {
                'svd__n_components': [29],
                # You can define other parameters to search here if needed
            }
        },
    ]

    results = []

    for model_info in models:
        with mlflow.start_run(run_name=model_info['name']):
            grid_search = GridSearchCV(model_info['estimator'], model_info['param_grid'])
            grid_search.fit(X_train, y_train)

            best_params = grid_search.best_params_
            print(f"Best parameters for model {model_info['name']}: {best_params}")

            best_model = grid_search.best_estimator_

            y_pred = best_model.predict(X_test)
            rmse = mean_squared_error(y_test, y_pred, squared=False)

            mlflow.set_tag("model", model_info['name'])
            mlflow.log_params(best_params)
            mlflow.log_metrics({
                "RMSE": rmse
            })
            mlflow.sklearn.log_model(best_model, "model")

            print(f"RMSE for {model_info['name']}: {rmse}")
            results.append((model_info['name'], rmse))

    return results

results = train_and_evaluate_models(X_train, X_test, y_train, y_test)

print('Recuperation des RMSE des modèles:')
for model_name, rmse in results:
    print(f"{model_name}: {rmse}")
