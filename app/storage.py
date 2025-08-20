from typing import Dict
from .models import Task


class TaskStorage:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}

    def add(self, task: Task):
        self.tasks[task.id] = task

    def get(self, task_id: str):
        return self.tasks.get(task_id)

    def get_all(self):
        return list(self.tasks.values())

    def update(self, task_id: str, **kwargs):
        task = self.tasks.get(task_id)
        if not task:
            return None
        for key, value in kwargs.items():
            if hasattr(task, key) and value is not None:
                setattr(task, key, value)
        return task

    def delete(self, task_id: str):
        return self.tasks.pop(task_id, None)
