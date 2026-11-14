from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import DatabaseUnavailableError

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(api_router, prefix="/api/v1")


@app.exception_handler(DatabaseUnavailableError)
async def handle_database_unavailable(
    request: Request, exc: DatabaseUnavailableError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"detail": str(exc)}
    )
