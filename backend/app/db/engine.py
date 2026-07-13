from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.core.config import get_settings


def create_database_engine(database_url: str | None = None) -> Engine:
    """Create the synchronous SQLAlchemy database engine."""

    settings = get_settings()
    resolved_database_url = database_url or settings.database_url

    return create_engine(
        resolved_database_url,
        pool_pre_ping=True,
    )


engine = create_database_engine()
