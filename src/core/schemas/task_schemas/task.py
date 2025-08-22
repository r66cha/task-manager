"""Task schemas."""

# -- Imports

from fastapi import Form
from pydantic import BaseModel, Field
from typing import Optional
import enum
from uuid import UUID


# -- Exports

__all__ = [
    "TaskStatus",
    "TaskBase",
    "TaskOut",
]

# -- Constants

CREATED = "Создано."
IN_PROGRESS = "В процессе..."
COMPLETED = "Выполнил!"

# -- Enums


class TaskStatus(str, enum.Enum):
    created = CREATED
    in_progress = IN_PROGRESS
    completed = COMPLETED


# --


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = ""

    @classmethod
    def as_form(
        cls,
        title: str = Form(..., description="Заголовок таски"),
        description: str = Form("", description="Описание таски"),
    ):
        return cls(title=title, description=description)

    # python-multipart


class TaskOut(TaskBase):
    id: UUID
    status: TaskStatus

    model_config = {"from_attributes": True}
