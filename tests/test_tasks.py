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
def mock_task_crud(monkeypatch):
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


# --


def test_create(mock_task_crud):

    app.dependency_overrides[get_task_crud] = lambda: mock_task_crud

    payload = {
        "task_title": TASK_TITLE,
        "task_description": TASK_DESCRIPTION,
    }
    response = client.post("/tasks/v1/", data=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == TASK_TITLE
    assert data["description"] == TASK_DESCRIPTION
    assert data["status"] == TASK_STATUS

    app.dependency_overrides = {}


# def test_update(mock_task_crud):
#     payload = {
#         "task_title": TASK_UUID,
#         "task_title": TASK_TITLE,
#         "task_description": TASK_DESCRIPTION,
#         "task_description": TASK_DESCRIPTION,
#     }
#     response = client.put(f"/tasks/v1/update/{TASK_UUID}", data=payload)
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert data["id"] == TASK_UUID
#     assert data["title"] == TASK_TITLE
#     assert data["description"] == TASK_DESCRIPTION
#     assert data["status"] == TASK_STATUS
