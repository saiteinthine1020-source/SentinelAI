from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.dependencies import get_db_session
from app.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter(tags=["Health"])

DatabaseSession = Annotated[Session, Depends(get_db_session)]


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check backend process health",
)
def health_check() -> HealthResponse:
    """Return basic process health without checking dependencies."""

    settings = get_settings()

    return HealthResponse(
        status="ok",
        service="sentinelai-backend",
        version=settings.app_version,
        environment=settings.app_env,
    )


@router.get(
    "/health/ready",
    response_model=ReadinessResponse,
    summary="Check backend database readiness",
)
def readiness_check(session: DatabaseSession) -> ReadinessResponse:
    """Confirm that the backend can query PostgreSQL."""

    try:
        session.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is unavailable",
        ) from exc

    return ReadinessResponse(
        status="ready",
        database="available",
    )
