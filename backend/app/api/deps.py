from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.repositories.health import HealthRepository
from app.services.health import HealthService


def get_db() -> Iterator[Session]:
    """Yield one session per request; the with block closes it afterwards, even on errors."""
    with SessionLocal() as session:
        yield session


def get_health_service(db: Annotated[Session, Depends(get_db)]) -> HealthService:
    return HealthService(HealthRepository(db))
