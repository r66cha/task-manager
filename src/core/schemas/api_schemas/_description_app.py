"""Description App."""

# -- Imports

from pydantic import BaseModel

# -- Exports

__all__ = ["DescriptionAppSchema"]

#


class DescriptionAppSchema(BaseModel):
    title: str = "Task manager"
    description: str = "Task manager for FastAPI"
    version: str = "1.0.0"
