from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check backend process health",
)
def health_check() -> HealthResponse:
    """Return basic process health without exposing sensitive settings."""

    settings = get_settings()

    return HealthResponse(
        status="ok",
        service="sentinelai-backend",
        version=settings.app_version,
        environment=settings.app_env,
    )
