"""Task schemas."""

# -- Imports

from pydantic import BaseModel, Field
from typing import Optional
import enum

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
    title: str = Field(..., example=TITLE_EXAMPLE)
    description: Optional[str] = Field("", example=DESCRIPTION_EXAMPLE)


class TaskCreate(TaskBase):
    pass


class TaskSchema(BaseModel):
    title: Optional[str] = Field(None, example=TITLE_EXAMPLE)
    description: Optional[str] = Field(None, example=DESCRIPTION_EXAMPLE)
    status: Optional[TaskStatus] = Field(None, example=TaskStatus.in_progress)


class TaskOut(TaskBase):
    id: str
    status: TaskStatus

    class Config:
        orm_mode = True
