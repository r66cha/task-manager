import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_task():
    response = client.post(
        "/tasks/", json={"title": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "created"
    assert "id" in data


def test_get_task():
    # Create a task first
    create_resp = client.post(
        "/tasks/", json={"title": "Get Task", "description": "Get Description"}
    )
    task_id = create_resp.json()["id"]

    # Get the task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Task"


def test_get_task_not_found():
    response = client.get("/tasks/nonexistent-id")
    assert response.status_code == 404


def test_list_tasks():
    # Create two tasks
    client.post("/tasks/", json={"title": "Task 1", "description": ""})
    client.post("/tasks/", json={"title": "Task 2", "description": ""})

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # There may be more from previous tests


def test_update_task():
    # Create a task
    create_resp = client.post(
        "/tasks/", json={"title": "To Update", "description": "Old"}
    )
    task_id = create_resp.json()["id"]

    # Update the task
    response = client.put(
        f"/tasks/{task_id}", json={"title": "Updated", "status": "in_progress"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["status"] == "in_progress"


def test_update_task_not_found():
    response = client.put("/tasks/nonexistent-id", json={"title": "Nope"})
    assert response.status_code == 404


def test_delete_task():
    # Create a task
    create_resp = client.post("/tasks/", json={"title": "To Delete", "description": ""})
    task_id = create_resp.json()["id"]

    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id

    # Ensure it's gone
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404


def test_delete_task_not_found():
    response = client.delete("/tasks/nonexistent-id")
    assert response.status_code == 404
