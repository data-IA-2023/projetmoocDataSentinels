from datetime import datetime
import streamlit as st
import pandas as pd
import joblib
import psycopg2
import os

# Connecter à la base de données
def connect_to_db():
    connection = psycopg2.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB")
    )
    return connection

# Obtenir les suggestions à partir de la base de données
@st.cache_resource
def get_suggestions_from_db(column_name):
    connection = connect_to_db()
    query = f"SELECT DISTINCT {column_name} FROM public.combined_view WHERE (username IS NOT NULL) AND (grade IS NOT NULL) AND (course_id IS NOT NULL) AND (course IS NOT NULL) AND (gender IS NOT NULL) AND (year_of_birth IS NOT NULL) AND (csp IS NOT NULL) AND (level_of_education IS NOT NULL);"
    suggestions = pd.read_sql(query, connection)[column_name].tolist()
    connection.close()
    return suggestions

# Chargement du modèle entraîné
@st.cache_resource
def load_model(model_path):
    model = joblib.load(model_path)
    return model

# Fonction pour faire des prédictions
def predict_grade(model, data):
    predictions = model.predict(data)
    return predictions

def calculate_age(X):
    current_year = datetime.now().year
    return current_year - X

def main():
    st.title("Prédiction du Grade")

    # Charger le modèle directement
    model_path = "RandomForestRegressor_model.joblib"
    model = load_model(model_path)

    # Obtenir les suggestions pour chaque attribut (une seule fois)
    courses = get_suggestions_from_db("course")
    bodyemotions = get_suggestions_from_db("bodyemotion")
    countries = get_suggestions_from_db("country")
    genders = get_suggestions_from_db("gender")
    csps = get_suggestions_from_db("csp")
    educations = get_suggestions_from_db("level_of_education")

    # Interface utilisateur pour saisir les informations nécessaires pour la prédiction
    st.header("Entrez les informations pour la prédiction")
    
    # Champs pour la saisie des informations
    course = st.selectbox("Cours", courses)
    bodyemotion = st.selectbox("Émotion du corps", bodyemotions)
    country = st.selectbox("Pays", countries)
    gender = st.selectbox("Genre", genders)
    year_of_birth = st.number_input("Année de naissance", min_value=1900, max_value=2024, value=2000)
    csp = st.selectbox("CSP", csps)
    level_of_education = st.selectbox("Niveau d'éducation", educations)

    # Préparer les données pour la prédiction
    new_data = pd.DataFrame({
        'course': [course],
        'bodyemotion': [bodyemotion],
        'country': [country],
        'gender': [gender],
        'year_of_birth': [year_of_birth],
        'csp': [csp],
        'level_of_education': [level_of_education]
    })

    if st.button("Prédire"):
        prediction = predict_grade(model, new_data)
        st.success(f"La prédiction de la note est : {prediction}")

if __name__ == "__main__":
    main()
