# test_postgresql_connection.py
import os
import pytest
import psycopg2
import dotenv

dotenv.load_dotenv()

@pytest.fixture
def postgresql_connection():
    print(os.environ)
    dbname = os.environ.get("POSTGRES_DB")
    
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")
    host = os.environ.get("POSTGRES_HOST")
    port = os.environ.get("POSTGRES_PORT", 5432)

    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    yield conn
    conn.close()

def test_postgresql_connection(postgresql_connection):
    cursor = postgresql_connection.cursor()
    cursor.execute("SELECT 1")
    assert cursor.fetchone() == (1,)
    cursor.close()

if __name__ == "__main__":
    pytest.main()
