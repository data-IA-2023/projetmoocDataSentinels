# ==============================
# import 
# ==============================
import streamlit as st
from bs4 import BeautifulSoup
import codecs
from streamlit_option_menu import option_menu
import base64

# ==============================
# run : streamlit run c:/Users/sandy/Documents/devIA/brief/mooc/projetmoocDataSentinels/main.py
# ==============================
st.set_page_config(
    page_title="Fun Mooc",
    page_icon="./static/logo.png",
)

# ==============================
# variable de session
# ==============================


# ==============================
# charge le css
# ==============================
with open( "./static/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


# ==============================
# fond d'écran
# ==============================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    page_bg_img = '''
    <style>
    .stApp {
    background-color: rgb(0, 106, 180);
    background-size: cover;
    font-family: "Turret Road";
    }
    [data-testid="stAppViewBlockContainer"]{
    background-color: rgb(200, 200, 200);
    font-family: "Tilt Neon";
    }
    </style>
    '''

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('./static/fond.png')


# ==============================
# bannière
# ==============================
def set_png_as_page_banner(png_file):
    bin_str_banner = get_base64_of_bin_file(png_file)
    page_banner_img = ''' 
    <style>
    [data-testid="stHeader"]{
    background-position: center;
    background-image: url("data:image/png;base64,%s");
    background-size: contain;
    background-repeat: no-repeat;
    }
    </style>
    ''' % bin_str_banner

    st.markdown(page_banner_img, unsafe_allow_html=True)
    return

set_png_as_page_banner('./static/banner.png')


# ==============================
# bar de navigation
# ==============================
def lancement():
    choix = option_menu(
        None, ["Home", "Analyse",  "Contact"], 
        icons=['house', 'cloud-upload', "list-task"], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important", "background-color": "rgb(150, 150, 150)"
            },
            "icon": {
                "color": "rgb(200, 200, 200)", "font-size": "15px"
            }, 
            "nav-link": {
                "color": "rgb(200, 200, 200)", "font-size": "15px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"
            },
            "nav-link-selected": {
                "color": "rgb(250, 250, 250)", "background-color": "rgb(0, 106, 180)"
            },
        }
    )

    if choix == "Home":
        # switch_page("Analytics")
        st.title("Home")
        st.write("")
        st.write("Bienvenu sur l'Appli de Fun Mooc !")
        st.write("")
        st.write("Rendez-vous sur la page Analyse pour voir si un étudiant à des chance de réussir sa formation.")
        st.write("Rendez-vous sur la page Contact pour plus d'information.")
        st.write("")
        st.write("")
        st.write("")
    if choix == "Analyse":
        # switch_page("Contact")
        st.title("Formulaire et Analyse")
    if choix == "Contact":
        # switch_page("Contact")
        st.title("Contact")

lancement()

# ==============================
# formulaire 
# ==============================

# champs à remplir

# bouton de validation


# ==============================
# traitement du formulaire
# ==============================

# quand le formulaire est validé : 3 boulton apparesse

# bouton de l'annalyse de la candidature

# bouton de l'analyse du message

# bouton de la FAQ et de recherche de topic


# ==============================
# 
# ==============================
# # Sidebar content
# st.sidebar.header("Sidebar Title")
# st.sidebar.subheader("Subheading")
# st.sidebar.write("Sidebar content goes here.")
