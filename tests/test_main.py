import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Main import app, Base, get_db

os.environ["DATABASE_URL"] = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:3891123@db_test:5432/test_db")
engine = create_engine(os.getenv("DATABASE_URL"))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
@app.get("/")
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
@app.get("/tasks/")
def test_post():
    item_data = {
        "Task": "<SOMETASK>",
    }
    response = client.post("/tasks/create_task", json=item_data)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    created_item = response.json()
    assert created_item["Task"] == "<SOMETASK>", "Task in response does not match sent data"
    print("Test passed successfully!")