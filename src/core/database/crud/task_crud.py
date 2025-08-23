"""CRUD"""

# --- Imports

import logging
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database.models import Task
from src.core.schemas.task_schemas import TaskOut, TaskBase, TaskStatus
from uuid import UUID
from fastapi import HTTPException, status


# -- Exports

__all__ = [
    "get_task_crud",
    "TaskCRUD",
]

# --

log = logging.getLogger(__name__)


# --


class TaskCRUD:

    async def create_task(
        self,
        session: AsyncSession,
        task_title: str,
        task_description: str,
    ) -> TaskOut:

        task = Task(title=task_title, description=task_description)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return TaskOut.model_validate(task)

    async def update_task(
        self,
        session: AsyncSession,
        task_uuid: UUID,
        task_title: str,
        task_description: str,
        task_status: TaskStatus,
    ) -> TaskOut:

        result = await session.execute(select(Task).where(Task.id == task_uuid))
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        task.title = task_title
        task.description = task_description
        task.status = task_status

        await session.commit()

        return task

    async def update_task_status(
        self,
        session: AsyncSession,
        task_uuid: UUID,
        task_status: TaskStatus,
    ) -> TaskOut:

        result = await session.execute(select(Task).where(Task.id == task_uuid))
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found",
            )

        task.status = task_status

        await session.commit()

        return task.status.value

    async def get_task(
        self,
        session: AsyncSession,
        task_uuid: UUID,
    ):

        result = await session.execute(select(Task).where(Task.id == task_uuid))

        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=404,
                detail=f"Task {task_uuid} not found",
            )

        return task

    async def get_all_tasks(
        self,
        session: AsyncSession,
    ) -> list:

        result = await session.execute(select(Task))
        tasks = result.scalars().all()
        return tasks

    async def delete_task(
        self,
        session: AsyncSession,
        task_uuid: UUID,
    ) -> bool:

        deleted = await session.execute(select(Task).where(Task.id == task_uuid))
        task = deleted.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail=f"Task {task_uuid} not found")

        await session.delete(task)
        await session.commit()

        return True


async def get_task_crud():
    return TaskCRUD()
