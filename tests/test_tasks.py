"""Tests."""

# -- Imports

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from src.core.schemas.task_schemas import TaskBase, TaskOut, TaskStatus
from src.core.database.crud import TaskCRUD
from fastapi import status

from typing import Any

from src.api.v1.server.app import app

from unittest.mock import AsyncMock, MagicMock

from src.api.v1.server.routers.task_router import get_task_crud


client = TestClient(app)

# --

BASE_URL = "http://127.0.0.1:8000/tasks/v1/"
TASK_UUID = "0f1e86a5-caf6-40d3-8210-b6bc35003c7b"  # нужно указать актуальный uuid
TASK_TITLE = "Тестовое задание"
TASK_DESCRIPTION = "Разработать task-manager"
TASK_STATUS = TaskStatus.created

TASK_CRUD_MP_PATH = "src.api.v1.server.routers.task_router.TaskCRUD"


# -- Fixtures


@pytest.fixture
def mock_create(monkeypatch):
    mock_crud: TaskCRUD = MagicMock(spec=TaskCRUD)
    task_out = TaskOut(
        id=TASK_UUID,
        title=TASK_TITLE,
        description=TASK_DESCRIPTION,
        status=TASK_STATUS,
    )
    mock_crud.create_task = AsyncMock(return_value=task_out)
    monkeypatch.setattr(TASK_CRUD_MP_PATH, lambda: mock_crud)
    return mock_crud


@pytest.fixture
def mock_update(monkeypatch):
    mock_crud: TaskCRUD = MagicMock(spec=TaskCRUD)
    task_out = TaskOut(
        id=TASK_UUID,
        title=TASK_TITLE,
        description=TASK_DESCRIPTION,
        status=TaskStatus.in_progress.value,
    )
    mock_crud.update_task = AsyncMock(return_value=task_out)
    monkeypatch.setattr(TASK_CRUD_MP_PATH, lambda: mock_crud)
    return mock_crud


@pytest.fixture
def mock_update_status(monkeypatch):
    mock_crud: TaskCRUD = MagicMock(spec=TaskCRUD)

    mock_crud.update_task_status = AsyncMock(return_value=TaskStatus.completed.value)
    monkeypatch.setattr(TASK_CRUD_MP_PATH, lambda: mock_crud)
    return mock_crud


@pytest.fixture
def mock_get_task(monkeypatch):
    mock_crud: TaskCRUD = MagicMock(spec=TaskCRUD)
    task_out = TaskOut(
        id=TASK_UUID,
        title=TASK_TITLE,
        description=TASK_DESCRIPTION,
        status=TaskStatus.completed.value,
    )
    mock_crud.get_task = AsyncMock(return_value=task_out)
    monkeypatch.setattr(TASK_CRUD_MP_PATH, lambda: mock_crud)
    return mock_crud


@pytest.fixture
def mock_get_all_task(monkeypatch):
    mock_crud: TaskCRUD = MagicMock(spec=TaskCRUD)
    task_out = TaskOut(
        id=TASK_UUID,
        title=TASK_TITLE,
        description=TASK_DESCRIPTION,
        status=TaskStatus.completed.value,
    )
    mock_crud.get_all_tasks = AsyncMock(return_value=[task_out])
    monkeypatch.setattr(TASK_CRUD_MP_PATH, lambda: mock_crud)
    return mock_crud


@pytest.fixture
def mock_delete(monkeypatch):
    mock_crud: TaskCRUD = MagicMock(spec=TaskCRUD)
    mock_crud.delete_task = AsyncMock(return_value=True)
    monkeypatch.setattr(TASK_CRUD_MP_PATH, lambda: mock_crud)
    return mock_crud


# --


def test_create(mock_create):

    app.dependency_overrides[get_task_crud] = lambda: mock_create

    payload = {
        "task_title": TASK_TITLE,
        "task_description": TASK_DESCRIPTION,
    }
    response = client.post("/tasks/v1/", data=payload)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["title"] == TASK_TITLE
    assert data["description"] == TASK_DESCRIPTION
    assert data["status"] == TASK_STATUS

    app.dependency_overrides = {}


def test_update(mock_update):

    app.dependency_overrides[get_task_crud] = lambda: mock_update

    payload = {
        "task_uuid": TASK_UUID,
        "task_title": TASK_TITLE,
        "task_description": TASK_DESCRIPTION,
        "task_status": TaskStatus.in_progress.value,
    }
    response = client.put(f"/tasks/v1/update/{TASK_UUID}", data=payload)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == TASK_UUID
    assert data["title"] == TASK_TITLE
    assert data["description"] == TASK_DESCRIPTION
    assert data["status"] == TaskStatus.in_progress.value

    app.dependency_overrides = {}


def test_update_status(mock_update_status):

    app.dependency_overrides[get_task_crud] = lambda: mock_update_status

    payload = {"task_status": TaskStatus.completed.value}
    response = client.patch(f"/tasks/v1/update-status/{TASK_UUID}", data=payload)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert (
        data["message"]
        == f"Статус таски {TASK_UUID} изменен на {TaskStatus.completed.value}!"
    )

    app.dependency_overrides = {}


def test_get_task(mock_get_task):

    app.dependency_overrides[get_task_crud] = lambda: mock_get_task

    response = client.get(f"/tasks/v1/{TASK_UUID}")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == TASK_UUID
    assert data["title"] == TASK_TITLE
    assert data["description"] == TASK_DESCRIPTION
    assert data["status"] == TaskStatus.completed.value

    app.dependency_overrides = {}


def test_get_all_task(mock_get_all_task):

    app.dependency_overrides[get_task_crud] = lambda: mock_get_all_task

    response = client.get(f"/tasks/v1/all")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(data, list)
    assert len(data) == 1

    task = data[0]

    assert task["id"] == TASK_UUID
    assert task["title"] == TASK_TITLE
    assert task["description"] == TASK_DESCRIPTION
    assert task["status"] == TaskStatus.completed.value

    app.dependency_overrides = {}


def test_delete(mock_delete):

    app.dependency_overrides[get_task_crud] = lambda: mock_delete

    response = client.delete(f"/tasks/v1/delete/{TASK_UUID}")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["message"] == f"Таска {TASK_UUID} успешно удалена!"

    app.dependency_overrides = {}
