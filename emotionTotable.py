import psycopg2
from deep_translator import GoogleTranslator
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
from langdetect import detect, LangDetectException
from Sentiment_analysis import translate_and_analyse
import os
from tqdm import tqdm

# Connexion à la base de données
connection = psycopg2.connect(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB")
)
cur = connection.cursor()

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")

def truncate_text_to_512_tokens(text):
    # Ensure the text is tokenized to a max length of 512 tokens
    tokens = tokenizer.encode(text, max_length=512, truncation=True)
    # Decode the tokens back to text
    return tokenizer.decode(tokens, skip_special_tokens=True)

# Sélection des lignes à traiter
cur.execute("SELECT id, body FROM public.message WHERE body IS NOT NULL AND bodyemotion IS NULL")
rows = cur.fetchall()

# Mise à jour de chaque ligne avec l'émotion détectée
for row in tqdm(rows, desc="Processing messages"):
    message_id, body_text = row
    
    # Check if the text is empty or too short to process
    if not body_text or len(body_text.strip()) == 0:
        continue
    
    truncated_text = truncate_text_to_512_tokens(body_text)
    
    # Handle language detection errors
    try:
        emotion_data = translate_and_analyse(truncated_text)
        emotion = emotion_data.get('emotion') if emotion_data else None
    except LangDetectException:
        print(f"Skipping message id {message_id}: unable to detect language.")
        continue
    
    if emotion:
        cur.execute(
            "UPDATE public.message SET bodyemotion = %s WHERE id = %s",
            (emotion, message_id)
        )

    # Commit des transactions et fermeture de la connexion
    connection.commit()

cur.close()
connection.close()

print("Mise à jour terminée.")
