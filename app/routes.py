from fastapi import APIRouter, HTTPException, status
from typing import List
from .schemas import TaskCreate, TaskUpdate, TaskOut
from .crud import create_task, get_task, get_tasks, update_task, delete_task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create(task_in: TaskCreate):
    task = create_task(task_in)
    return TaskOut(
        id=task.id, title=task.title, description=task.description, status=task.status
    )


@router.get("/", response_model=List[TaskOut])
def list_tasks():
    return [
        TaskOut(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
        )
        for task in get_tasks()
    ]


@router.get("/{task_id}", response_model=TaskOut)
def get(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut(
        id=task.id, title=task.title, description=task.description, status=task.status
    )


@router.put("/{task_id}", response_model=TaskOut)
def update(task_id: str, task_in: TaskUpdate):
    task = update_task(task_id, task_in)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut(
        id=task.id, title=task.title, description=task.description, status=task.status
    )


@router.delete("/{task_id}", response_model=TaskOut)
def delete(task_id: str):
    task = delete_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut(
        id=task.id, title=task.title, description=task.description, status=task.status
    )
