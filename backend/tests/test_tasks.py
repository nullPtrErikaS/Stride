# tests/test_tasks.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture()
def authorized_client(client):
    # Register a user
    client.post("/auth/register", json={
        "username": "taskuser",
        "email": "taskuser@example.com",
        "password": "taskpassword"
    })
    # Login the user
    response = client.post("/auth/login", json={
        "email": "taskuser@example.com",
        "password": "taskpassword"
    })
    access_token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client

def test_create_task(authorized_client):
    response = authorized_client.post("/tasks/", json={"content": "My first task!"})
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "My first task!"

def test_get_tasks(authorized_client):
    # Create a task first
    authorized_client.post("/tasks/", json={"content": "Another task"})
    response = authorized_client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_update_task(authorized_client):
    # Create a task
    response = authorized_client.post("/tasks/", json={"content": "Update me!"})
    task_id = response.json()["id"]

    # Update the task
    response = authorized_client.put(f"/tasks/{task_id}", json={"content": "I have been updated"})
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "I have been updated"

def test_delete_task(authorized_client):
    # Create a task
    response = authorized_client.post("/tasks/", json={"content": "Delete me!"})
    task_id = response.json()["id"]

    # Delete the task
    response = authorized_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"
