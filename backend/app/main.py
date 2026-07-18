import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_v1_router, root_router
from app.core.config import Settings, get_settings
from app.core.logging import configure_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Handle application startup and shutdown events."""

    settings = get_settings()

    logger.info(
        "Starting %s version %s in %s environment",
        settings.app_name,
        settings.app_version,
        settings.app_env,
    )

    yield

    logger.info("Stopping %s", settings.app_name)


def create_application(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""

    configure_logging()

    application_settings = settings or get_settings()

    application = FastAPI(
        title=application_settings.app_name,
        version=application_settings.app_version,
        description=("Backend API for the SentinelAI security and observability platform."),
        debug=application_settings.debug,
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=application_settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Accept"],
    )

    application.include_router(root_router)
    application.include_router(
        api_v1_router,
        prefix=application_settings.api_v1_prefix,
    )

    return application


app = create_application()
