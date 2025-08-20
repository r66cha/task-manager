from pydantic import BaseModel, Field
from typing import Optional
from .models import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(..., example="Buy groceries")
    description: Optional[str] = Field("", example="Milk, Bread, Eggs")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Buy groceries")
    description: Optional[str] = Field(None, example="Milk, Bread, Eggs")
    status: Optional[TaskStatus] = Field(None, example="in_progress")


class TaskOut(TaskBase):
    id: str
    status: TaskStatus

    class Config:
        orm_mode = True
