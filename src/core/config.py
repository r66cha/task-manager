"""Application configuration module."""

# -- Imports

from pydantic_settings import BaseSettings
from src.core.schemas import DescriptionAppSchema
from src.core.schemas.api_schemas import DatabaseConfigSchema, ApiSchema

# -- Exports

__all__ = ["settings"]

# --


class Settings(BaseSettings):
    """Main application settings."""

    _description: DescriptionAppSchema = DescriptionAppSchema()
    db: DatabaseConfigSchema = DatabaseConfigSchema()
    api: ApiSchema = ApiSchema()


settings = Settings()
