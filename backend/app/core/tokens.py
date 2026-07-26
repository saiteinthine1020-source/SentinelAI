from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import BaseModel, ValidationError

from app.core.config import get_settings


class AccessTokenPayload(BaseModel):
    """Validated data extracted from a JWT access token."""

    sub: UUID
    type: str
    iat: datetime
    exp: datetime


class TokenExpiredError(Exception):
    """Raised when an access token has expired."""


class TokenInvalidError(Exception):
    """Raised when an access token is malformed or invalid."""


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


def decode_access_token(token: str) -> AccessTokenPayload:
    """Decode and validate a JWT access token."""

    settings = get_settings()

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            options={
                "require": ["sub", "type", "iat", "exp"],
            },
        )

        validated_payload = AccessTokenPayload.model_validate(payload)

    except ExpiredSignatureError as exc:
        raise TokenExpiredError from exc

    except (InvalidTokenError, ValidationError, ValueError) as exc:
        raise TokenInvalidError from exc

    if validated_payload.type != "access":
        raise TokenInvalidError

    return validated_payload
