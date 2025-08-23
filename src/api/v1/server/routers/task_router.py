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
from src.core.config import settings


log = logging.getLogger(__name__)


# -- Exports

__all__ = ["tr"]

# --

tr = APIRouter(
    prefix=settings.api.v1_data_url,
    tags=["tasks"],
)

DESC_UUID = "Заголовок таски"
DESC_TITLE = "Уникальный идентификатор таски (UUID)"
DESC_DESCRIPTION = "Описание таски"
DESC_STATUS = "Новый статус таски"

# --


@tr.post(
    path="/",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    name="crete-task",
)
async def create(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[TaskCRUD, Depends(get_task_crud)],
    task_title: str = Form("", description=DESC_TITLE),
    task_description: str = Form("", description=DESC_DESCRIPTION),
):
    """Создает таску."""

    return await task_crud.create_task(session, task_title, task_description)


@tr.put(
    path="/update/{task_uuid}",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
    name="update",
)
async def update(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[TaskCRUD, Depends(get_task_crud)],
    task_uuid: UUID = Path(..., description=DESC_UUID),
    task_title: str = Form("", description=DESC_TITLE),
    task_description: str = Form("", description=DESC_DESCRIPTION),
    task_status: TaskStatus = Form(..., description=DESC_STATUS),
):
    """Обновляет данные таски."""

    return await task_crud.update_task(
        session,
        task_uuid,
        task_title,
        task_description,
        task_status,
    )


@tr.patch(
    path="/update-status/{task_uuid}",
    status_code=status.HTTP_200_OK,
    name="update status",
)
async def update_status(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[TaskCRUD, Depends(get_task_crud)],
    task_uuid: UUID = Path(..., description=DESC_UUID),
    task_status: TaskStatus = Form(..., description=DESC_STATUS),
):
    """Обновляет статус таски."""

    new_status = await task_crud.update_task_status(session, task_uuid, task_status)
    return {"message": f"Статус таски {task_uuid} изменен на {new_status}!"}


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

    return await task_crud.get_all_tasks(session)


@tr.get(
    path="/{task_uuid}",
    response_model=TaskOut,
    name="get task",
)
async def get_task(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[TaskCRUD, Depends(get_task_crud)],
    task_uuid: UUID = Path(..., description=DESC_UUID),
):
    """Отдает таску по uuid."""

    return await task_crud.get_task(session, task_uuid)


@tr.delete(
    path="/delete/{task_uuid}",
    name="delete task",
)
async def delete_task(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[TaskCRUD, Depends(get_task_crud)],
    task_uuid: UUID = Path(..., description=DESC_UUID),
):
    """Удаляет таску по uuid."""

    await task_crud.delete_task(session, task_uuid)
    return {"message": f"Таска {task_uuid} успешно удалена!"}
