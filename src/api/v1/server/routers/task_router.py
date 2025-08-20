"""Task router."""

# -- Import

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import db_manager
from src.core.schemas.task_schemas import TaskOut, TaskSchema
from src.core.database.crud import TaskCRUD, get_task_crud


# -- Exports

__all__ = ["tr"]

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
    task_data: TaskSchema,
):

    task: TaskOut = await task_crud.create_task(session, task_data)
    return TaskOut(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
    )
