import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Connect to the PostgreSQL database in one line
connection = psycopg2.connect(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB")
)

# Check connection
cursor = connection.cursor()
cursor.execute("SELECT version();")
db_version = cursor.fetchone()
print(f"Connected to PostgreSQL database. Version: {db_version}")

# Close connection
cursor.close()
connection.close()
print("PostgreSQL connection is closed")