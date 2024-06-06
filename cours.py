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

# Créer la table 'course' dans PostgreSQL si elle n'existe pas déjà
create_course_table_query = '''
CREATE TABLE IF NOT EXISTS course (
    course_id VARCHAR(100) PRIMARY KEY,
    univ VARCHAR(100),
    course VARCHAR(100),
    session VARCHAR(100),
    temps_alloue VARCHAR(50)
);
'''
cursor.execute(create_course_table_query)
connection.commit()

# Créer la table 'result' dans PostgreSQL si elle n'existe pas déjà
create_result_table_query = '''
CREATE TABLE IF NOT EXISTS result (
    username VARCHAR(200) NOT NULL,
    course_id VARCHAR(100) NOT NULL,
    grade FLOAT,
    Certificate_Eligible VARCHAR(100),
    Certificate_Delivered VARCHAR(100),
    Certificate_Type VARCHAR(100),
    date_grade_report VARCHAR(50),
    PRIMARY KEY (username, course_id)
);
'''
cursor.execute(create_result_table_query)
connection.commit()

def courseExtracteur(doc, cursor, connection):
    for key, value in doc.items():
        if isinstance(value, dict) and key != '_id':
            course_id = key
            opening_date = value.get('opening_date', None)

            # Extracting univ, course, and session from course_id
            course_id = course_id.replace('course-v1:', '')
            info = course_id.split('+' if '+' in course_id else '/')
            univ = info[0] if len(info) > 0 else None
            course = info[1] if len(info) > 1 else None
            session = info[2] if len(info) > 2 else None
            # Extracting temps_alloue
            temps_alloue = value.get('tempsAlloue', None)
            
            
            # Insertion des données dans PostgreSQL
            insert_course_query = '''
            INSERT INTO course (course_id, univ, course, session, temps_alloue)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (course_id) DO NOTHING;
            '''
            cursor.execute(insert_course_query, (course_id, univ, course, session, temps_alloue))
            
            # Valider la transaction
            connection.commit()

def resultExtracteur(doc, cursor, connection):
    username = doc.get('username', None)
    if not username:
        return  # Ignore the document if username is None or empty

    for key, value in doc.items():
        if isinstance(value, dict) and key != '_id':
            course_id = key
            grade = float(value.get('grade', 0.0)) if value.get('grade') else None
            certificate_eligible = value.get('Certificate Eligible', None)
            certificate_delivered = value.get('Certificate Delivered', None)
            certificate_type = value.get('Certificate Type', None)
            date_grade_report = value.get('date_grade_report', None)
            # Insertion des données dans PostgreSQL
            insert_result_query = '''
            INSERT INTO result (username, course_id, grade, Certificate_Eligible, Certificate_Delivered, Certificate_Type, date_grade_report)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (username, course_id) DO NOTHING;
            '''
            cursor.execute(insert_result_query, (username, course_id, grade, certificate_eligible, certificate_delivered, certificate_type, date_grade_report))
            
            # Valider la transaction
            connection.commit()

# Extraire les données de MongoDB et les insérer dans PostgreSQL
for doc in tqdm(user_collection.find()):
    courseExtracteur(doc, cursor, connection)
    resultExtracteur(doc, cursor, connection)

# Fermer les connexions
cursor.close()
connection.close()
client.close()
print("Données insérées avec succès dans PostgreSQL.")
