"""Module containing mixins for SQLAlchemy ORM models."""

# -- Imports

from sqlalchemy.orm import Mapped, mapped_column


# --


class IdIntPkMixin:
    """Mixin with the 'id' field as an integer primary key."""

    id: Mapped[int] = mapped_column(primary_key=True)
