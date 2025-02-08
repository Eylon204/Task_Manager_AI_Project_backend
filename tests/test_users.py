import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user():
    """Tests creating a new user via API."""
    user_data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "securepassword"
    }
    response = client.post("/users/create", json=user_data)
    assert response.status_code == 201
    assert "id" in response.json()


def test_get_user():
    """Tests retrieving user details via API."""
    user_id = "existing_user_id"  # Replace with a valid ID
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"


def test_update_user():
    """Tests updating an existing user via API."""
    user_id = "existing_user_id"  # Replace with a valid ID
    update_data = {"email": "updated@example.com"}
    response = client.put(f"/users/update/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["email"] == "updated@example.com"


def test_delete_user():
    """Tests deleting a user via API."""
    user_id = "existing_user_id"  # Replace with a valid ID
    response = client.delete(f"/users/delete/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}
