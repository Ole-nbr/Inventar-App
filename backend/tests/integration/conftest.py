from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.session import engine
from app.main import app

ALEMBIC_INI = Path(__file__).resolve().parents[2] / "alembic.ini"


@pytest.fixture(scope="session")
def migrated_database() -> None:
    """Bring the test database schema up to date once per test run."""
    # Guard against ever migrating or writing to a non-test database.
    assert engine.url.database is not None and engine.url.database.endswith("_test")
    command.upgrade(Config(str(ALEMBIC_INI)), "head")


@pytest.fixture
def db_session(migrated_database: None) -> Iterator[Session]:
    """Session inside an outer transaction that is rolled back after each test.

    Commits in the code under test only release a savepoint, so no test sees
    data from another test.
    """
    with engine.connect() as connection, connection.begin() as transaction:
        session = Session(bind=connection, join_transaction_mode="create_savepoint")
        yield session
        session.close()
        transaction.rollback()


@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    app.dependency_overrides[get_db] = lambda: db_session
    yield TestClient(app)
    app.dependency_overrides.clear()
