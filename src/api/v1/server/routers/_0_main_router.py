"""Main router."""

# -- Imports

from fastapi import APIRouter
from .task_router import tr
from src.core.config import settings

# -- Exports

__all__ = ["main_router"]

# --


main_router = APIRouter(prefix=settings.api.prefix)
main_router.include_router(tr)
