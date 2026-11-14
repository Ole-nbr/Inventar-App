from unittest.mock import create_autospec

import pytest
from sqlalchemy.exc import OperationalError

from app.core.exceptions import DatabaseUnavailableError
from app.repositories.health import HealthRepository
from app.services.health import HealthService


def test_check_database_passes_when_ping_succeeds() -> None:
    repository = create_autospec(HealthRepository, instance=True)

    HealthService(repository).check_database()

    repository.ping.assert_called_once_with()


def test_check_database_raises_domain_error_when_ping_fails() -> None:
    repository = create_autospec(HealthRepository, instance=True)
    repository.ping.side_effect = OperationalError("SELECT 1", {}, Exception("connection refused"))

    with pytest.raises(DatabaseUnavailableError):
        HealthService(repository).check_database()
