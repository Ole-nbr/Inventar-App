from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_health_service
from app.schemas.health import HealthRead
from app.services.health import HealthService

router = APIRouter()


@router.get("/health", response_model=HealthRead)
def get_health() -> HealthRead:
    return HealthRead(status="ok")


@router.get("/health/db", response_model=HealthRead)
def get_database_health(
    service: Annotated[HealthService, Depends(get_health_service)],
) -> HealthRead:
    service.check_database()
    return HealthRead(status="ok")
