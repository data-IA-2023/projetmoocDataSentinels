# ==============================
# import 
# ==============================
import streamlit as st
from streamlitGrade import get_suggestions_from_db

# ==============================
# variable de session
# ==============================

# traitement du bouton de formulaire
def click_formulaire():
    st.session_state.formulaire = True

if "formulaire" not in st.session_state:
    st.session_state.formulaire = False

# ==============================
# formulaire 
# ==============================
CHOICES = {"01002":"Du manager au leader : devenir agile et collaboratif",
            "04026":"S'initier à la fabrication numérique", 
            "04017":"Programmer un objet avec un Arduino",
            "04021":"Imprimer en 3D",
            "04018":"Fabriquer un objet connecté"}

def format_func(option):
    return CHOICES[option]

def formulaire () :
    # champs à remplir
    st.header("Formulaire pour les estimations :")

    # courses = get_suggestions_from_db("course")
    # bodyemotions = get_suggestions_from_db("bodyemotion")
    # countries = get_suggestions_from_db("country")
    # genders = get_suggestions_from_db("gender")
    # csps = get_suggestions_from_db("csp")
    # educations = get_suggestions_from_db("level_of_education")

    # st.write("courses :", "bodyemotions :", "countries :", "genders :", "csps :", "educations :")
    # st.write(courses, bodyemotions, countries, genders, csps, educations)
    
    with st.form("Formulaire pour les estimations :"):
        new_user = st.text_input("choisi ton nom d'utilisateur :", value="Morty")
        new_mooc = st.selectbox( "Choisi la formation visée", options=list(CHOICES.keys()), format_func=format_func)#, value=courses)
        new_genre = st.selectbox("choisi ton genre :", ("none","f","m"))#, value=genders)
        new_contry = st.selectbox( "Choisi ton pay", ("fr", "TN", "LB", "GA", "SN", "DZ", "RE", "MA", "NE", "HT", "CN", "BJ", "CD"))#, Value=countries)
        new_age = st.number_input("Choisi ta date de naissence", min_value=1900, max_value=2024, value=2000, step =1)
        new_level_educ = st.selectbox("choisi ton niveau de diplome :", ("none","m","hs", "jhs", "b", "p", "a", "other"))#, value=educations)
        new_csp = st.selectbox("choisi ton statut :", 
                               ("none","Cadre, sup","Retraité", "Sans", "Etudiant", "Employé", "Prof interm", 
                                "Enseugnant", "Artisan, commerçant ou chef d'entreprise", "Recherche emploi"))#, value=csps)
        new_message = st.text_input("Entre le message à poster sur le forum", value="cool ce cours !")
        
        st.form_submit_button("Valider", on_click=click_formulaire)

    # bouton de validation
    if st.session_state.formulaire == True :
        if not new_user :
            st.sidebar.error("Tu dois renseigner un nom d'utilisateur")
        if not new_mooc :
            st.sidebar.error("Tu dois renseigner la formation")
        if not new_genre :
            st.sidebar.error("Tu dois renseigner ton genre")
        if not new_contry :
            st.sidebar.error("Tu dois renseigner ton pay")
        if not new_age :
            st.sidebar.error("Tu dois renseigner ta date de naissence")
        if not new_level_educ :
            st.sidebar.error("Tu dois renseigner ton niveau de diplome")
        if not new_csp :
            st.sidebar.error("Tu dois renseigner ton statut")
        if not new_message :
            st.sidebar.error("Tu dois renseigner un message pour le forum")

        if new_user and new_mooc and new_genre and new_contry and new_age and new_level_educ and new_csp and new_message :
            return {"new_user":new_user, "new_mooc":new_mooc, "new_genre":new_genre, "new_contry":new_contry,
                     "new_age":new_age, "new_level_educ":new_level_educ, "new_csp":new_csp, "new_message":new_message}
