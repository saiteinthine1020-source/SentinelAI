from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
import pytest

from app.core.config import get_settings
from app.core.tokens import (
    TokenExpiredError,
    TokenInvalidError,
    create_access_token,
    decode_access_token,
)


def test_create_access_token_contains_expected_claims() -> None:
    settings = get_settings()
    user_id = uuid4()

    token = create_access_token(
        user_id=user_id,
        expires_minutes=30,
    )

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload["sub"] == str(user_id)
    assert payload["type"] == "access"
    assert "iat" in payload
    assert "exp" in payload


def test_decode_access_token_returns_validated_payload() -> None:
    user_id = uuid4()
    token = create_access_token(user_id=user_id)

    payload = decode_access_token(token)

    assert payload.sub == user_id
    assert payload.type == "access"


def test_decode_access_token_rejects_expired_token() -> None:
    settings = get_settings()
    now = datetime.now(UTC)

    token = jwt.encode(
        {
            "sub": str(uuid4()),
            "type": "access",
            "iat": now - timedelta(minutes=10),
            "exp": now - timedelta(minutes=5),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(TokenExpiredError):
        decode_access_token(token)


def test_decode_access_token_rejects_invalid_signature() -> None:
    settings = get_settings()
    now = datetime.now(UTC)

    token = jwt.encode(
        {
            "sub": str(uuid4()),
            "type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=30),
        },
        "incorrect-secret",
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(TokenInvalidError):
        decode_access_token(token)


def test_decode_access_token_rejects_wrong_token_type() -> None:
    settings = get_settings()
    now = datetime.now(UTC)

    token = jwt.encode(
        {
            "sub": str(uuid4()),
            "type": "refresh",
            "iat": now,
            "exp": now + timedelta(minutes=30),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(TokenInvalidError):
        decode_access_token(token)


def test_decode_access_token_rejects_invalid_subject() -> None:
    settings = get_settings()
    now = datetime.now(UTC)

    token = jwt.encode(
        {
            "sub": "not-a-uuid",
            "type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=30),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(TokenInvalidError):
        decode_access_token(token)
