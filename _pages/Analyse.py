# ==============================
# import 
# ==============================
import streamlit as st
from Sentiment_analysis import translate_and_analyse
from FAQVECT import topic_FAQ
from streamlitGrade import grade_prediction

# ==============================
# variable de session
# ==============================

# traitement du bouton d'annalyse de la candidature
def click_annalyse_candidature():
    st.session_state.candidature = True

if "annalyse de la candidature" not in st.session_state:
    st.session_state.candidature = False

# traitement du bouton de formulaire
def click_analyse_message():
    st.session_state.message = True

if "analyse du message" not in st.session_state:
    st.session_state.message = False

# traitement du bouton de formulaire
def click_topic_FAQ():
    st.session_state.topic_FAQ = True

if "recherche de topic et FAQ" not in st.session_state:
    st.session_state.topic_FAQ = False

# ==============================
# traitement du formulaire
# ==============================
def analyse (dict) :
    # teste le dict
    # st.write(dict)
    if dict == False :
        st.sidebar.error("Les informations du formulaire ne sont pas disponible, merci de remplir le formulaire.")

    else :
        # quand le formulaire est validé : 3 boulton apparesse
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("annalyse de la candidature", on_click=click_annalyse_candidature)
        with col2:
            st.button("analyse du message", on_click=click_analyse_message)
        with col3:
            st.button("recherche de topic et FAQ", on_click=click_topic_FAQ)

        # bouton de l'analyse du message
        if st.session_state.message == True :
            st.header("Analyse du message")
            texte = dict["new_message"]
            emotion_labels = translate_and_analyse(texte)
            st.write("l'analyse de l'émotion du message donne :")
            st.write(emotion_labels)

        # bouton de l'annalyse de la candidature
        if st.session_state.candidature == True :
            st.header("Annalyse de la candidature :")
            emotion_labels = translate_and_analyse(dict["new_message"])
            emotion = emotion_labels["emotion"]
            dict["new_emotion"] = emotion
            grade_prediction(dict)

        # bouton de la FAQ et de recherche de topic
        if st.session_state.topic_FAQ == True :
            st.header("Recherche de topic et FAQ :")
            texte = dict["new_message"]
            topic_FAQ (texte)


            