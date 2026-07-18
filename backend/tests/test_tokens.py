from uuid import uuid4

import jwt

from app.core.config import get_settings
from app.core.tokens import create_access_token


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
