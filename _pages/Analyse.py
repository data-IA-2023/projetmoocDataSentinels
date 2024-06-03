# ==============================
# import 
# ==============================
import streamlit as st

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
def formulaire () :
    # champs à remplir
    st.header("Formulaire pour les estimations :")

    with st.form("Formulaire pour les estimations :"):
        new_user = st.text_input("choisis ton nom d'utilisateur :", value="Morty")
        new_mooc = st.selectbox( "Choisi la formation visée",
                                ("S'initier à la fabrication numérique", 
                                 "Programmer un objet avec un Arduino", 
                                 "Imprimer en 3D",
                                 "Modéliser en 3D avec FreeCAD",
                                 "Fabriquer un objet connecté"))
        new_message = st.text_input("Entre le message à poster sur le forum", value="bla bla bla")
        # new_startYear = st.slider("En quelle année le film va sortir", min_value=1850.0, max_value=2100.0, step =1.0, value=2018.0)
        st.form_submit_button("Valider", on_click=click_formulaire)

    # bouton de validation
    if st.session_state.formulaire == True :

        if not new_user :
            st.sidebar.error("Tu dois renseigner un nom d'utilisateur")
        if not new_mooc :
            st.sidebar.error("Tu dois renseigner la formation")
        if not new_message :
            st.sidebar.error("Tu dois renseigner un message pour le forum")

        if new_user and new_mooc and new_message :
            return {"new_user":new_user, "new_mooc" : new_mooc, "new_message" : new_message}


# ==============================
# traitement du formulaire
# ==============================

# quand le formulaire est validé : 3 boulton apparesse

# bouton de l'annalyse de la candidature

# bouton de l'analyse du message

# bouton de la FAQ et de recherche de topic