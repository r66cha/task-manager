"""Task router."""

# -- Import

import logging
from fastapi import APIRouter, Depends, HTTPException, status, Form, Path
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.schemas.task_schemas import TaskOut, TaskBase, TaskStatus
from src.core.database.crud import TaskCRUD, get_task_crud
from uuid import UUID
from src.core.database import db_manager


# -- Exports

__all__ = ["tr"]

# --

log = logging.getLogger(__name__)

# --

tr = APIRouter(prefix="/tasks", tags=["tasks"])


@tr.post(
    path="/",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    name="crete-task",
)
async def create(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[TaskCRUD, Depends(get_task_crud)],
    task_base: Annotated[TaskBase, Depends(TaskBase.as_form)],
):
    """Создает таску"""

    try:
        task: TaskOut = await task_crud.create_task(session, task_base)
        return task
    except HTTPException as http_exc:
        log.error("Exception: %s", http_exc)
    except Exception as e:
        log.error("Exception: %s", e)


@tr.put(
    path="/update",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
    name="update",
)
async def update(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[TaskCRUD, Depends(get_task_crud)],
    task_uuid: UUID,
    task_title: str = Form(""),
    task_description: str = Form(""),
    task_status: TaskStatus = TaskStatus.created,
):
    """Обновляет данные таски."""

    try:
        task: TaskOut = await task_crud.update_task(
            session,
            task_uuid,
            task_title,
            task_description,
            task_status,
        )
        return task
    except HTTPException as http_exc:
        log.error("Exception: %s", http_exc)
    except Exception as e:
        log.error("Exception: %s", e)


@tr.get(
    path="/all",
    response_model=List[TaskOut],
    name="get all tasks",
)
async def get_all_tasks(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[TaskCRUD, Depends(get_task_crud)],
) -> List[TaskOut]:
    """Отдает список тасок."""

    try:

        return await task_crud.get_all_tasks(session)

    except HTTPException as http_exc:
        log.error("Exception: %s", http_exc)
    except Exception as e:
        log.error("Exception: %s", e)


@tr.get(
    path="/{task_uuid}",
    response_model=TaskOut,
    name="get task",
)
async def get_task(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[TaskCRUD, Depends(get_task_crud)],
    task_uuid: UUID = Path(..., title="UUID таски"),
):
    """Отдает таску по uuid."""

    try:

        task: TaskOut = await task_crud.get_task(session, task_uuid)
        return task

    except HTTPException as http_exc:
        log.error("Exception: %s", http_exc)
    except Exception as e:
        log.error("Exception: %s", e)


@tr.delete(
    path="/delete/{task_uuid}",
    name="get task",
)
async def delete_task(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[TaskCRUD, Depends(get_task_crud)],
    task_uuid: UUID = Path(..., title="UUID таски"),
):
    """Удаляет таску по uuid."""

    try:

        deleted: bool = await task_crud.delete_task(session, task_uuid)

        if not deleted:
            raise HTTPException(status_code=404, detail=f"Task {task_uuid} not found")

        return {"message": f"Task {task_uuid} deleted successfully"}

    except HTTPException as http_exc:
        log.error("Exception: %s", http_exc)
    except Exception as e:
        log.error("Exception: %s", e)
