"""CRUD module"""

# --- Imports

import logging
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database.models import Task
from src.core.schemas.task_schemas import TaskOut, TaskBase, TaskStatus
from uuid import UUID
from fastapi import HTTPException


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
        task_data: TaskBase,
    ) -> TaskOut:

        try:

            task = Task(**task_data.model_dump())
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return TaskOut.model_validate(task)

        except Exception as e:
            log.error("Exception: %s", e)

    async def update_task(
        self,
        session: AsyncSession,
        task_uuid: UUID,
        task_title: str,
        task_description: str,
        task_status: TaskStatus,
    ) -> TaskOut:

        try:

            result = await session.execute(select(Task).where(Task.id == task_uuid))
            task = result.scalar_one_or_none()

            if not task:
                raise HTTPException(status_code=404, detail="Task not found")

            task.title = task_title
            task.description = task_description
            task.status = task_status

            await session.commit()

            return task

        except Exception as e:
            log.error("Exception: %s", e)

    async def update_task_status(
        self,
        session: AsyncSession,
        task_uuid: UUID,
        task_status: TaskStatus,
    ) -> TaskOut:

        try:

            result = await session.execute(select(Task).where(Task.id == task_uuid))
            task = result.scalar_one_or_none()

            if not task:
                raise HTTPException(status_code=404, detail="Task not found")

            task.status = task_status

            await session.commit()
            await session.refresh(task)

            return task

        except Exception as e:
            log.error("Exception: %s", e)

    async def get_task(
        self,
        session: AsyncSession,
        task_uuid: UUID,
    ):

        try:

            result = await session.execute(select(Task).where(Task.id == task_uuid))
            task = result.scalar_one_or_none()
            return task

        except Exception as e:
            log.error("Exception: %s", e)

    async def get_all_tasks(
        self,
        session: AsyncSession,
    ):

        try:

            result = await session.execute(select(Task))
            tasks = result.scalars().all()
            return tasks

        except Exception as e:
            log.error("Exception: %s", e)

    async def delete_task(
        self,
        session: AsyncSession,
        task_uuid: UUID,
    ) -> bool:

        try:

            result = await session.execute(select(Task).where(Task.id == task_uuid))
            task = result.scalar_one_or_none()

            if not task:
                return False

            await session.delete(task)
            await session.commit()

            return True

        except Exception as e:
            log.error("Exception: %s", e)


async def get_task_crud():
    return TaskCRUD()
