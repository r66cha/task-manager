"""Database models module"""

# -- Imports

import uuid
from sqlalchemy import Integer, String, String, Enum as SqlEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from src.core.database.mixin.mx import IdIntPkMixin
from sqlalchemy.dialects.postgresql import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas.task_schemas.task import TaskStatus

# -- Exports

__all__ = ["Task"]

# --


class Base(DeclarativeBase):
    pass


class Task(Base, IdIntPkMixin):
    """Tasks database model"""

    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        String,
        default=TaskStatus.created,
        nullable=True,
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        """Returns an instance of TaskDatabaseClass."""
