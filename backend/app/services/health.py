from sqlalchemy.exc import OperationalError

from app.core.exceptions import DatabaseUnavailableError
from app.repositories.health import HealthRepository


class HealthService:
    """Checks whether the services the application depends on are available."""

    def __init__(self, repository: HealthRepository) -> None:
        self._repository = repository

    def check_database(self) -> None:
        """Raise DatabaseUnavailableError if the database cannot be reached."""
        try:
            self._repository.ping()
        except OperationalError as exc:
            raise DatabaseUnavailableError("Database is not reachable") from exc
