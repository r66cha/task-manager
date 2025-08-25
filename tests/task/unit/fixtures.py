"""Tests."""

# -- Imports

import pytest
from src.core.schemas.task_schemas import TaskOut, TaskStatus
from src.core.database.crud import TaskCRUD
from unittest.mock import AsyncMock, MagicMock


# -- Exports

__all__ = [
    "mock_create",
    "mock_update",
    "mock_update_status",
    "mock_get_task",
    "mock_get_all_task",
    "mock_delete",
]

# --

BASE_URL = "http://127.0.0.1:8000/tasks/v1/"
TASK_UUID = "0f1e86a5-caf6-40d3-8210-b6bc35003c7b"
TASK_TITLE = "Тестовое задание"
TASK_DESCRIPTION = "Разработать task-manager"
TASK_STATUS = TaskStatus.created

TASK_CRUD_MP_PATH = "src.api.v1.server.routers.task_router.TaskCRUD"


# --


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
