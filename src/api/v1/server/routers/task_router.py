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

tr = APIRouter(tags=["tasks"])


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
        log.error("HTTPException: %s", http_exc)
    except Exception as e:
        log.error("Exception: %s", e)


@tr.put(
    path="/update/{task_uuid}",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
    name="update",
)
async def update(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[TaskCRUD, Depends(get_task_crud)],
    task_uuid: UUID = Path(..., description="Уникальный идентификатор таски (UUID)"),
    task_title: str = Form("", description="Заголовок таски"),
    task_description: str = Form("", description="Описание таски"),
    task_status: TaskStatus = Form(..., description="Новый статус таски"),
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
        log.error("HTTPException: %s", http_exc)
    except Exception as e:
        log.error("Exception: %s", e)


@tr.patch(
    path="/update-status/{task_uuid}",
    status_code=status.HTTP_200_OK,
    name="update status",
)
async def update_status(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[TaskCRUD, Depends(get_task_crud)],
    task_uuid: UUID = Path(..., description="Уникальный идентификатор таски (UUID)"),
    task_status: TaskStatus = Form(..., description="Новый статус таски"),
):
    try:
        new_status = await task_crud.update_task_status(session, task_uuid, task_status)
        return {f"Статус таски {task_uuid} изменен на {new_status}!"}

    except HTTPException as http_exc:
        log.error("HTTPException: %s", http_exc)
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
        log.error("HTTPException: %s", http_exc)
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
    task_uuid: UUID = Path(..., description="Уникальный идентификатор таски (UUID)"),
):
    """Отдает таску по uuid."""

    return await task_crud.get_task(session, task_uuid)


@tr.delete(
    path="/delete/{task_uuid}",
    name="get task",
)
async def delete_task(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[TaskCRUD, Depends(get_task_crud)],
    task_uuid: UUID = Path(..., description="Уникальный идентификатор таски (UUID)"),
):
    """Удаляет таску по uuid."""

    await task_crud.delete_task(session, task_uuid)
    return {"message": f"Task {task_uuid} deleted successfully"}
