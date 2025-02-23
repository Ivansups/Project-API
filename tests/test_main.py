from fastapi.testclient import TestClient
from app.Main import app
from app.schemas import TaskCreate

client = TestClient(app)


def test_create_task():
    task_data = TaskCreate(Task="Test Task")

    response = client.post("/tasks/create_task", json=task_data.model_dump())

    assert response.status_code == 200
    data = response.json()
    assert data["Task"] == task_data.Task
    assert "id" in data and isinstance(data["id"], int)


def test_update_task():
    create_response = client.post("/tasks/create_task", json=TaskCreate(Task="Initial Task").model_dump())
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]
    assert task_id is not None

    update_data = TaskCreate(Task="Updated Task")
    update_response = client.put(f"/tasks/update_task_by_id/{task_id}", json=update_data.model_dump())
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["Task"] == update_data.Task


def test_delete_task():
    create_response = client.post("/tasks/create_task", json=TaskCreate(Task="Task to Delete").model_dump())
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]
    assert task_id is not None

    delete_response = client.delete(f"/tasks/delete_task_by_id/{task_id}")
    assert delete_response.status_code == 200
    deleted_data = delete_response.json()
    assert deleted_data["id"] == task_id