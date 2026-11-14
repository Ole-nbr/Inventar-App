from unittest.mock import create_autospec

from fastapi.testclient import TestClient

from app.api.deps import get_health_service
from app.core.exceptions import DatabaseUnavailableError
from app.main import app
from app.services.health import HealthService


def test_get_database_health_returns_ok_when_database_is_reachable(client: TestClient) -> None:
    response = client.get("/api/v1/health/db")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_database_health_returns_503_when_database_is_unreachable(
    client: TestClient,
) -> None:
    service = create_autospec(HealthService, instance=True)
    service.check_database.side_effect = DatabaseUnavailableError("Database is not reachable")
    app.dependency_overrides[get_health_service] = lambda: service

    response = client.get("/api/v1/health/db")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database is not reachable"}
