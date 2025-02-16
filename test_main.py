from fastapi.testclient import TestClient
from Main import app
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_post():
    item_data = {
        "Task": "<SOMETASK>",
    }
    response = client.post("/post", json=item_data)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    created_item = response.json()
    assert created_item["Task"] == "<SOMETASK>" "Task in response does not match sent data"
    print("Test passed successfully!")