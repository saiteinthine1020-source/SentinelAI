from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.tokens import create_access_token
from app.models.user import User

ME_ENDPOINT = "/api/v1/auth/me"
COOKIE_NAME = "sentinelai_access_token"


def create_user(
    db_session: Session,
    *,
    email: str = "current.user@example.com",
    is_active: bool = True,
) -> User:
    user = User(
        username="current_user",
        email=email,
        password_hash="not-used-by-current-user-tests",
        is_active=is_active,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def test_current_user_returns_public_user(
    client: TestClient,
    db_session: Session,
) -> None:
    user = create_user(db_session)
    token = create_access_token(user_id=user.id)

    client.cookies.set(COOKIE_NAME, token)

    response = client.get(ME_ENDPOINT)
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == str(user.id)
    assert body["username"] == "current_user"
    assert body["email"] == "current.user@example.com"
    assert body["is_active"] is True
    assert "created_at" in body
    assert "password_hash" not in body


def test_current_user_rejects_missing_cookie(
    client: TestClient,
) -> None:
    response = client.get(ME_ENDPOINT)

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication required"}


def test_current_user_rejects_invalid_token(
    client: TestClient,
) -> None:
    client.cookies.set(COOKIE_NAME, "invalid-token")

    response = client.get(ME_ENDPOINT)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or expired authentication session"}


def test_current_user_rejects_expired_token(
    client: TestClient,
) -> None:
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

    client.cookies.set(COOKIE_NAME, token)

    response = client.get(ME_ENDPOINT)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or expired authentication session"}


def test_current_user_rejects_unknown_user(
    client: TestClient,
) -> None:
    token = create_access_token(user_id=uuid4())
    client.cookies.set(COOKIE_NAME, token)

    response = client.get(ME_ENDPOINT)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authentication session"}


def test_current_user_rejects_inactive_user(
    client: TestClient,
    db_session: Session,
) -> None:
    user = create_user(
        db_session,
        email="inactive.current@example.com",
        is_active=False,
    )

    token = create_access_token(user_id=user.id)
    client.cookies.set(COOKIE_NAME, token)

    response = client.get(ME_ENDPOINT)

    assert response.status_code == 403
    assert response.json() == {"detail": "Account access is disabled"}
