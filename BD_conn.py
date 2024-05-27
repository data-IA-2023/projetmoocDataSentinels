from pymongo import MongoClient
import psycopg2
import dotenv
import os
from tqdm import tqdm

def conection () :
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

    return cursor