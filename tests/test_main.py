import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Main import app
from app.db import Base, get_db
from app.crud import create_task
from app.models import Task
from app.schemas import TaskCreate

os.environ["TEST_DATABASE_URL"] = "postgresql://postgres:3891123@localhost:5432/my_db"
os.environ["DATABASE_URL"] = os.getenv("TEST_DATABASE_URL")

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

def test_create_task():
    task_data = TaskCreate(Task="Test Task")
    response = client.post("/tasks/create_task", json=task_data.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert data["Task"] == task_data.Task
    assert "id" in data and isinstance(data["id"], int)

def test_update_task():
    create_response = client.post("/tasks/create_task", json={"Task": "Initial Task"})
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]
    assert task_id is not None

    update_response = client.put(f"/tasks/update_task_by_id/{task_id}", json={"Task": "Updated Task"})
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["Task"] == "Updated Task"

def test_delete_task():
    create_response = client.post("/tasks/create_task", json={"Task": "Task to Delete"})
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]
    assert task_id is not None

    delete_response = client.delete(f"/tasks/delete_task_by_id/{task_id}")
    assert delete_response.status_code == 200
    deleted_data = delete_response.json()
    assert deleted_data["id"] == task_id

def test_get_all_tasks():
    with TestingSessionLocal() as db:
        create_task(db, TaskCreate(Task="Task 1"))
        create_task(db, TaskCreate(Task="Task 2"))

    response = client.get("/tasks/get_all_tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

def teardown_module():
    with TestingSessionLocal() as db:
        db.query(Task).delete()
        db.commit()