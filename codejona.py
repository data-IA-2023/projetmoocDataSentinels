import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.base import BaseEstimator, TransformerMixin
from datetime import datetime
import mlflow
import mlflow.sklearn
from sqlalchemy import create_engine, inspect
import joblib
import os
import psycopg2
# Configuration de la connexion à la base de données

# Connexion à la base de données

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
            LIMIT 10;
"""
df = pd.read_sql(query, connection)            
connection.close()            

print(df)
print(df.dtypes)


df['embedding']=df['embedding'].apply(eval)

print(df['embedding'].to_numpy())

def calculate_age(X):
    current_year = datetime.now().year
    return current_year - X

# def convert_embedding_string_to_list(embedding_str):
#     # Convertir une chaîne d'embedding en liste de valeurs
#     return np.array([float(x) for x in embedding_str.strip('{}').split(',')])

# # Convertir les embeddings en listes de valeurs numériques
# df['embedding'] = df['embedding'].apply(convert_embedding_string_to_list)

# Example embedding function to transform embeddings to separate columns
class EmbeddingTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Assuming X is a DataFrame and embeddings are in a single column
        return np.vstack(X.apply(lambda x: np.array(x), axis=1))

X = df[['course', 'embedding', 'bodyemotion', 'country', 'gender', 'year_of_birth', 'csp', 'level_of_education']]
y = df['grade'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numeric_features = ['year_of_birth']
categorical_features = ['course', 'bodyemotion', 'country', 'gender', 'csp', 'level_of_education']
embedding_feature = ['embedding']

# Numeric transformer
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('age_calculator', FunctionTransformer(calculate_age, validate=False)),
    ('scaler', StandardScaler())
])

# Categorical transformer
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')), 
    ('onehot', OneHotEncoder(drop='first'))
])

# Embedding transformer
embedding_transformer = Pipeline(steps=[
    ('embed_transformer', EmbeddingTransformer()),
    ('scaler', StandardScaler())
])

# Combine all transformers into a single ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features),
        ('emb', embedding_transformer, embedding_feature)
    ]
)

mlflow.set_tracking_uri("file:./mlruns")

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    models = [
        {
            "name": "DecisionTree",
            "estimator": Pipeline(steps=[
                ('preprocessor', preprocessor), 
                ('classifier', DecisionTreeClassifier(random_state=42))
            ]),
            "param_grid": { 
                'classifier__max_depth': [3, 5, 7, None],
                'classifier__min_samples_split': [2, 5, 10],
                'classifier__min_samples_leaf': [1, 2, 4]
            } 
        },
        {
            "name": "RandomForest",
            "estimator": Pipeline(steps=[
                ('preprocessor', preprocessor), 
                ('classifier', RandomForestClassifier(random_state=42))
            ]),
            "param_grid": { 
                'classifier__n_estimators': [50, 100, 200],
                'classifier__max_depth': [3, 5, 7, None],
                'classifier__min_samples_split': [2, 5, 10],
                'classifier__min_samples_leaf': [1, 2, 4]
            } 
        },
        {
            "name": "LogisticRegression",
            "estimator": Pipeline(steps=[
                ('preprocessor', preprocessor), 
                ('classifier', LogisticRegression(max_iter=1000, random_state=42))
            ]),
            "param_grid": { 
                'classifier__C': [0.01, 0.1, 1, 10, 100],
                'classifier__penalty': ['l1', 'l2'],
                'classifier__solver': ['liblinear'],
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
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            precision = precision_score(y_test, y_pred, average='weighted')

            mlflow.set_tag("model", model_info['name'])
            mlflow.log_params(best_params)
            mlflow.log_metrics({
                "accuracy": accuracy,
                "f1_score": f1,
                "recall": recall,
                "precision": precision,
            })
            mlflow.sklearn.log_model(best_model, "model")

            # Sauvegarde du modèle avec joblib
            joblib.dump(best_model, f"{model_info['name']}_model.joblib")

            print(f"Accuracy for {model_info['name']}: {accuracy}")
            results.append((model_info['name'], accuracy))

    return results

results = train_and_evaluate_models(X_train, X_test, y_train, y_test)

print('Recuperation des accuracy des models:')
for model_name, accuracy in results:
    print(f"{model_name}: {accuracy}")

# Fonction pour charger un modèle sauvegardé et faire des prédictions
def load_model_and_predict(model_path, X_new):
    # Charger le modèle sauvegardé
    model = joblib.load(model_path)
    
    # Faire des prédictions
    predictions = model.predict(X_new)
    
    return predictions

# Exemple d'utilisation de la fonction de prédiction
# X_new est un DataFrame avec les nouvelles données
# predictions = load_model_and_predict("RandomForest_model.joblib", X_new)
