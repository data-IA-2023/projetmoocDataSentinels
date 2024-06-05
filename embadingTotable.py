import psycopg2
from transformers import CamembertModel, CamembertTokenizer
import torch
import numpy as np
import os
from tqdm import tqdm

# Connexion à la base de données
conn = psycopg2.connect(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB")
)
cur = conn.cursor()

# Create the extension if it doesn't exist
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
conn.commit()

# Créer la table pour stocker les embeddings si elle n'existe pas déjà
cur.execute("""
CREATE TABLE IF NOT EXISTS public.embeddings (
    id VARCHAR(100) PRIMARY KEY,
    embedding VECTOR(768) -- Assuming the vector length is 768
);
""")
conn.commit()

# Récupérer les données de la table message qui n'ont pas encore d'embeddings
cur.execute("""
SELECT m.id, m.body 
FROM public.message m 
LEFT JOIN public.embeddings e ON m.id = e.id 
WHERE e.id IS NULL
""")
rows = cur.fetchall()  # Fetch all rows first

# Itérer sur chaque ligne de la base de données
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

batch_size = 100  # Set your preferred batch size
batch_data = []

for row in tqdm(rows, desc="Traitement des messages"):
    # Extraire les données de la ligne
    message_id, body = row
    # Générer l'embedding pour le texte
    embedding = generate_embedding(body)

    # Convertir l'embedding en une chaîne de caractères au format '[...]'
    embedding_str = '[' + ','.join(map(str, embedding.flatten().tolist())) + ']'

    # Ajouter les données au batch
    batch_data.append((message_id, embedding_str))

    # Insérer en batch et commit
    if len(batch_data) >= batch_size:
        cur.executemany(
            "INSERT INTO public.embeddings (id, embedding) VALUES (%s, %s)",
            batch_data
        )
        conn.commit()
        batch_data = []

# Insert any remaining data
if batch_data:
    cur.executemany(
        "INSERT INTO public.embeddings (id, embedding) VALUES (%s, %s)",
        batch_data
    )
    conn.commit()

# Fermer la connexion
cur.close()
conn.close()
