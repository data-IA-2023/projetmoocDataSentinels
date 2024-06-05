import streamlit as st
import psycopg2
from transformers import CamembertModel, CamembertTokenizer
import torch
import numpy as np
import os
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
from nltk.corpus import stopwords

# Télécharger les stopwords français
nltk.download('stopwords')
french_stopwords = list(set(stopwords.words('french')))

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

# Extraction des features avec TfidfVectorizer
vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words=french_stopwords)

# Application de LDA pour le topic modeling
lda = LatentDirichletAllocation(n_components=10, random_state=0)

# Application de K-means pour le clustering
kmeans = KMeans(n_clusters=5, random_state=0)

# Interface Streamlit
st.title("FAQ")

input_text = st.text_area("Entrez le texte du message")

if st.button("Rechercher"):
    if input_text:
        # Générer l'embedding pour le texte d'entrée
        input_embedding = generate_embedding(input_text).reshape(1, -1)
        input_embedding_list = input_embedding.tolist()[0]
        input_embedding_str = ','.join(map(str, input_embedding_list))
        # Requête SQL pour trouver les trois messages les plus similaires
        query = f"""
        SELECT me.id, m.body, 1 - (me.embedding <=> '[{input_embedding_str}]'::vector) AS cosine_similarity
        FROM public.embeddings me
        JOIN public.message m ON me.id = m.id
        ORDER BY cosine_similarity DESC
        LIMIT 20;
        """
        cur.execute(query)
        results = cur.fetchall()
        
        if results:
            # Créer un dataframe pour afficher les résultats
            df = pd.DataFrame(results, columns=["ID du message", "Contenu du message", "Score de similarité"])
            
            # Topic modeling et clustering
            X = vectorizer.fit_transform(df['Contenu du message'])
            lda.fit(X)
            kmeans.fit(lda.transform(X))
            df['Topic'] = kmeans.labels_
            
            st.dataframe(df)
        else:
            st.write("Aucun message similaire trouvé.")
        
    else:
        st.write("Veuillez entrer un texte.")

# Fermer la connexion
cur.close()
conn.close()