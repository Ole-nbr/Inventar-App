from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve .env relative to this file, so it is found regardless of the working directory.
ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    """Application settings loaded from environment variables and the root .env file."""

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    app_name: str = "Inventar-App"
    environment: Literal["development", "production"] = "development"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    """Return the settings, loaded once and cached for the lifetime of the process."""
    return Settings()
