import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_task():
    """Tests creating a new task via API."""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "medium",
        "estimated_time": 60,
        "user_id": "test_user"
    }
    response = client.post("/tasks/", json=task_data)  # שונה ל- /tasks/
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_tasks():
    """Tests retrieving all tasks for a user via API."""
    response = client.get("/tasks?user_id=test_user")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_task():
    """Tests updating an existing task via API."""
    task_id = "existing_task_id"  # Replace with a valid ID
    update_data = {"priority": "high"}
    response = client.put(f"/tasks/{task_id}", json=update_data)  # שונה ל- /tasks/{task_id}
    assert response.status_code == 200
    assert response.json()["priority"] == "high"

def test_delete_task():
    """Tests deleting a task via API."""
    task_id = "existing_task_id"  # Replace with a valid ID
    response = client.delete(f"/tasks/{task_id}")  # שונה ל- /tasks/{task_id}
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}