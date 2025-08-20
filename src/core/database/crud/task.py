"""CRUD module"""

# --- Imports

from sqlalchemy.ext.asyncio import AsyncSession
from src.core.schemas.task_schemas import TaskSchema
from src.core.database.models import Task
from src.core.schemas.task_schemas import TaskOut

# -- Exports

__all__ = [
    "get_task_crud",
    "TaskCRUD",
]

# --


class TaskCRUD:

    async def create_task(
        session: AsyncSession,
        task_data: TaskSchema,
    ):
        task = Task(**task_data.model_dump())
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return TaskOut.model_validate(task)

    async def get_task(task_id: str, session: AsyncSession): ...
    async def get_tasks(session: AsyncSession): ...
    async def update_task(task_id: str, task_in, session: AsyncSession): ...
    async def delete_task(task_id: str, session: AsyncSession): ...


async def get_task_crud():
    return TaskCRUD()
