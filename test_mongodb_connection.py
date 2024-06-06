# test_mongodb_connection.py
import os
import pytest
from pymongo import MongoClient
import dotenv

dotenv.load_dotenv()

@pytest.fixture
def mongodb_client():
    mongo_url = os.environ.get("MONGO_URL")
    client = MongoClient(mongo_url)
    yield client
    client.close()

def test_mongodb_connection(mongodb_client):
    db = mongodb_client['mooc']
    assert db.command("ping") == {'ok': 1.0}

if __name__ == "__main__":
    pytest.main()
