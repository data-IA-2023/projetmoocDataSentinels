from pymongo import MongoClient
import psycopg2
import dotenv
import os
from tqdm import tqdm

# Charger les variables d'environnement
dotenv.load_dotenv()

# Connexion MongoDB
client = MongoClient(os.environ["MONGO_URL"])
user_collection = client['mooc']['user']

# Connexion PostgreSQL
connection = psycopg2.connect(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB")
)
cursor = connection.cursor()

# Créer la table 'users' dans PostgreSQL si elle n'existe pas déjà
create_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR PRIMARY KEY,
    country VARCHAR,
    gender VARCHAR,
    year_of_birth INTEGER,
    CSP VARCHAR,
    level_of_education VARCHAR,
    city VARCHAR,
    email VARCHAR
);
'''
cursor.execute(create_table_query)
connection.commit()

def userExtracteur(doc, cursor, connection):
    username = doc.get('username', None)
    if not username:
        return  # Ignore the document if username is None or empty

    country = None
    gender = None
    year_of_birth = None
    CSP = None
    level_of_education = None
    city = None
    email = None
    # Parcourir les champs pour extraire les informations pertinentes
    for key, value in doc.items():
        if isinstance(value, dict):
            if 'country' in value:
                country = value['country']
            if 'gender' in value:
                gender = value['gender']
            if 'year_of_birth' in value:
                year_of_birth = int(value['year_of_birth']) if value['year_of_birth'].isdigit() else None
            if 'CSP' in value:
                CSP = value['CSP']
            if 'level_of_education' in value:
                level_of_education = value['level_of_education']
            if 'city' in value:
                city = value['city']
            if 'email' in value:
                email = value['email']

    # Insertion des données dans PostgreSQL
    insert_query = '''
    INSERT INTO users (username, country, gender, year_of_birth, CSP, level_of_education, city, email)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (username) DO NOTHING;
    '''
    cursor.execute(insert_query, (username, country, gender, year_of_birth, CSP, level_of_education, city, email))
    
    # Valider la transaction
    connection.commit()

# Extraire les données de MongoDB et les insérer dans PostgreSQL
for doc in tqdm(user_collection.find()):
    userExtracteur(doc, cursor, connection)

# Fermer les connexions
cursor.close()
connection.close()
client.close()
print("Données insérées avec succès dans PostgreSQL.")
