"""Constants."""

# -- Imports

from src.core.schemas.task_schemas import TaskStatus


# -- Exports

l__ = [
    "BASE_URL",
    "TASK_UUID",
    "TASK_TITLE",
    "TASK_DESCRIPTION",
    "TASK_STATUS",
    "TASK_CRUD_MP_PATH",
]

# --

BASE_URL = "http://127.0.0.1:8000/tasks/v1/"
TASK_UUID = "0f1e86a5-caf6-40d3-8210-b6bc35003c7b"  # нужно указать актуальный uuid
TASK_TITLE = "Тестовое задание"
TASK_DESCRIPTION = "Разработать task-manager"
TASK_STATUS = TaskStatus.created

TASK_CRUD_MP_PATH = "src.api.v1.server.routers.task_router.TaskCRUD"
