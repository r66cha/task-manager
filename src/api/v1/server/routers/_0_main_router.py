"""Main router."""

# -- Imports

from fastapi import APIRouter
from .task_router import tr

# -- Exports

__all__ = ["main_router"]

# --


main_router = APIRouter()
main_router.include_router(tr)
