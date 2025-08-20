from .models import Task, TaskStatus
from .schemas import TaskCreate, TaskUpdate
from .storage import TaskStorage


storage = TaskStorage()


def create_task(task_in: TaskCreate) -> Task:
    task = Task(
        title=task_in.title,
        description=task_in.description or "",
        status=TaskStatus.created,
    )
    storage.add(task)
    return task


def get_task(task_id: str) -> Task:
    return storage.get(task_id)


def get_tasks() -> list[Task]:
    return storage.get_all()


def update_task(task_id: str, task_in: TaskUpdate) -> Task | None:
    update_data = task_in.dict(exclude_unset=True)
    return storage.update(task_id, **update_data)


def delete_task(task_id: str) -> Task | None:
    return storage.delete(task_id)
