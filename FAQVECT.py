import streamlit as st
import psycopg2
from transformers import CamembertModel, CamembertTokenizer
import torch
import numpy as np
import os
import pandas as pd

def topic_FAQ (input_text) :
    # Connexion à la base de données
    conn = psycopg2.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB")
    )
    cur = conn.cursor()

    # Charger le modèle et le tokenizer Camembert
    model_name = 'camembert-base'
    tokenizer = CamembertTokenizer.from_pretrained(model_name)
    model = CamembertModel.from_pretrained(model_name)

    # Fonction pour générer les embeddings
    def generate_embedding(text):
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        outputs = model(**inputs)
        # Utiliser les embeddings du token [CLS] pour représenter la phrase
        cls_embedding = outputs.last_hidden_state[:, 0, :].detach().numpy()
        return cls_embedding

    # # Interface Streamlit
    # st.title("FAQ")

    # input_text = st.text_area("Entrez le texte du message")

    
    # Générer l'embedding pour le texte d'entrée
    input_embedding = generate_embedding(input_text).reshape(1, -1)
    input_embedding_list = input_embedding.tolist()[0]
    input_embedding_str = ','.join(map(str, input_embedding_list))
    # Requête SQL pour trouver les trois messages les plus similaires
    query = f"""
    SELECT me.id, m.course_id, m.body, 1 - (me.embedding <=> '[{input_embedding_str}]'::vector) AS cosine_similarity
    FROM public.embeddings me
    JOIN public.message m ON me.id = m.id
    ORDER BY cosine_similarity DESC
    LIMIT 7;
    """
    cur.execute(query)
    results = cur.fetchall()
    
    if results:
        # Créer un dataframe pour afficher les résultats
        df = pd.DataFrame(results, columns=["ID du message", "Topic du message", "Contenu du message", "Score de similarité"])
        st.dataframe(df)
    else:
        st.write("Aucun message similaire trouvé.")
    

    # Fermer la connexion
    cur.close()
    conn.close()
