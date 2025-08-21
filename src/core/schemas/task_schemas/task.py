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
    "TaskSchema",
    "TaskBase",
    "TaskCreate",
    "TaskOut",
]

# -- Constants

CREATED = "created"
IN_PROGRESS = "in_progress"
COMPLETED = "completed"

TITLE_EXAMPLE = "Купить продукты"
DESCRIPTION_EXAMPLE = "Молоко, Хлеб, Яйца"

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
        title: str = Form(..., example=TITLE_EXAMPLE),
        description: str = Form("", example=DESCRIPTION_EXAMPLE),
    ):
        return cls(title=title, description=description)

    # python-multipart


class TaskCreate(TaskBase):
    pass


class TaskSchema(BaseModel):
    title: Optional[str] = Field(None, example=TITLE_EXAMPLE)
    description: Optional[str] = Field(None, example=DESCRIPTION_EXAMPLE)
    status: Optional[TaskStatus] = Field(None, example=TaskStatus.in_progress)


class TaskOut(TaskBase):
    id: UUID
    status: TaskStatus

    model_config = {"from_attributes": True}
