"""Database config."""

# -- Imports

from pydantic_settings import BaseSettings, SettingsConfigDict

# -- Exports

__all__ = ["db_url"]

# --


class DB_URL(BaseSettings):
    """
    Pydantic settings class for configuring database connection parameters.\n
    Reads values from an environment file and builds a complete async database URL.
    """

    # -- API

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # --

    dialect: str = "postgresql+asyncpg"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def get_DB_URL_API(self) -> str:
        """Construct the full database connection URL string."""

        return f"{self.dialect}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_PORT}:{self.DB_PORT}/{self.DB_NAME}"


db_url = DB_URL()
