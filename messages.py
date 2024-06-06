from pymongo import MongoClient
import psycopg2
import dotenv
import os
from tqdm import tqdm
from datetime import datetime

# Charger les variables d'environnement
dotenv.load_dotenv()

# Connexion MongoDB
client = MongoClient(os.environ["MONGO_URL"])
message_collection = client['mooc']['Message']

# Connexion PostgreSQL
connection = psycopg2.connect(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB")
)

cursor = connection.cursor()
drop_message_table_query = '''
DROP TABLE IF EXISTS message;
'''
cursor.execute(drop_message_table_query)
connection.commit()

# Créer la table 'message' dans PostgreSQL si elle n'existe pas déjà
create_message_table_query = '''
CREATE TABLE IF NOT EXISTS message (
    id VARCHAR(100) PRIMARY KEY,
    course_id VARCHAR(100),
    username VARCHAR(100),
    anonymous BOOLEAN,
    anonymous_to_peers BOOLEAN,
    niv INT,
    body TEXT,
    type_ VARCHAR(50),
    read BOOLEAN,
    resp_total INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    votes_down_count INT,
    votes_up_count INT
);
'''
cursor.execute(create_message_table_query)
connection.commit()

def clean_string(s):
    if s:
        return s.replace('\x00', '')  # Remove null characters
    return s

def messageExtracteur(doc, cursor, connection):
    # Extract message details
    id = str(doc.get('id', None))
    course_id = doc.get('course_id', None)
    niv = doc.get('niv', None)
    body = clean_string(doc.get('body', None))
    read = doc.get('read', None)
    resp_total = doc.get('resp_total', None)
    type_ = doc.get('type', None)
    created_at = doc.get('created_at', None)
    updated_at = doc.get('updated_at', None)
    username = clean_string(doc.get('username', None))
    anonymous = doc.get('anonymous', None)
    anonymous_to_peers = doc.get('anonymous_to_peers', None)
    
    votes_down_count = doc.get('votes', {}).get('down_count', None)
    votes_up_count = doc.get('votes', {}).get('up_count', None)

    # Convert timestamp strings to datetime objects
    if created_at:
        created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
    if updated_at:
        updated_at = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))


    # Insertion des données dans PostgreSQL
    insert_message_query = '''
        INSERT INTO message (
            id, course_id, username, anonymous, anonymous_to_peers, created_at, niv, body, read, resp_total, type_, updated_at, votes_down_count, votes_up_count
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    '''

    cursor.execute(insert_message_query, (
        id, course_id, username, anonymous, anonymous_to_peers, created_at, niv, body, read, resp_total, type_, updated_at, votes_down_count, votes_up_count
    ))
    
    # Valider la transaction
    connection.commit()

# Extraire les données de MongoDB et les insérer dans PostgreSQL
for doc in tqdm(message_collection.find()):
    messageExtracteur(doc, cursor, connection)

# Fermer les connexions
cursor.close()
connection.close()
client.close()
print("Données insérées avec succès dans PostgreSQL.")
