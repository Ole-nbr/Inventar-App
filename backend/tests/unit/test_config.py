from collections.abc import Iterator
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_settings

ENV_VARS = ("APP_NAME", "ENVIRONMENT", "DEBUG", "DATABASE_URL")
DATABASE_URL = "postgresql+psycopg://user:secret@localhost:5432/inventar"


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_settings_use_defaults_without_environment() -> None:
    settings = Settings(_env_file=None, database_url=DATABASE_URL)

    assert settings.app_name == "Inventar-App"
    assert settings.environment == "development"
    assert settings.debug is False


def test_settings_read_environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_NAME", "Test-App")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("DATABASE_URL", DATABASE_URL)

    settings = Settings(_env_file=None)

    assert settings.app_name == "Test-App"
    assert settings.environment == "production"
    assert settings.debug is True
    assert settings.database_url.get_secret_value() == DATABASE_URL


def test_settings_read_env_file(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(f"APP_NAME=From-File\nDEBUG=true\nDATABASE_URL={DATABASE_URL}\n")

    settings = Settings(_env_file=env_file)

    assert settings.app_name == "From-File"
    assert settings.debug is True
    assert settings.database_url.get_secret_value() == DATABASE_URL


def test_settings_reject_unknown_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "prod")

    with pytest.raises(ValidationError):
        Settings(_env_file=None, database_url=DATABASE_URL)


def test_settings_require_database_url() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_settings_hide_database_url_in_output() -> None:
    settings = Settings(_env_file=None, database_url=DATABASE_URL)

    assert "secret" not in repr(settings)


def test_get_settings_returns_cached_instance(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", DATABASE_URL)

    assert get_settings() is get_settings()
