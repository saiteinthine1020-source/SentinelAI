from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt

from app.core.config import get_settings


def create_access_token(
    *,
    user_id: UUID,
    expires_minutes: int | None = None,
) -> str:
    """Create a signed JWT access token."""

    settings = get_settings()
    now = datetime.now(UTC)

    expiration_minutes = (
        expires_minutes if expires_minutes is not None else settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=expiration_minutes),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
