import enum
import uuid


class TaskStatus(str, enum.Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"


class Task:
    def __init__(
        self,
        title: str,
        description: str,
        status: TaskStatus = TaskStatus.created,
    ):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.status = status
