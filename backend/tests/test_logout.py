from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.core.tokens import create_access_token
from app.models.user import User

LOGOUT_ENDPOINT = "/api/v1/auth/logout"
ME_ENDPOINT = "/api/v1/auth/me"
COOKIE_NAME = "sentinelai_access_token"


def create_user(db_session: Session) -> User:
    user = User(
        username="logout_user",
        email="logout.user@example.com",
        password_hash=hash_password("StrongPassword123!"),
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def test_logout_clears_authentication_cookie(
    client: TestClient,
    db_session: Session,
) -> None:
    user = create_user(db_session)
    token = create_access_token(user_id=user.id)

    client.cookies.set(COOKIE_NAME, token)

    authenticated_response = client.get(ME_ENDPOINT)

    assert authenticated_response.status_code == 200

    logout_response = client.post(LOGOUT_ENDPOINT)

    assert logout_response.status_code == 200
    assert logout_response.json() == {"message": "Logout successful"}

    set_cookie = logout_response.headers["set-cookie"]

    assert "sentinelai_access_token=" in set_cookie
    assert "Max-Age=0" in set_cookie
    assert "Path=/" in set_cookie


def test_logout_succeeds_without_cookie(
    client: TestClient,
) -> None:
    response = client.post(LOGOUT_ENDPOINT)

    assert response.status_code == 200
    assert response.json() == {"message": "Logout successful"}


def test_logout_is_idempotent(
    client: TestClient,
) -> None:
    first_response = client.post(LOGOUT_ENDPOINT)
    second_response = client.post(LOGOUT_ENDPOINT)

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    assert first_response.json() == {"message": "Logout successful"}
    assert second_response.json() == {"message": "Logout successful"}


def test_logout_does_not_return_token(
    client: TestClient,
) -> None:
    response = client.post(LOGOUT_ENDPOINT)

    body = response.json()

    assert "token" not in body
    assert "access_token" not in body
    assert "cookie" not in body


def test_logout_succeeds_with_invalid_cookie(
    client: TestClient,
) -> None:
    client.cookies.set(
        COOKIE_NAME,
        "invalid-token-value",
    )

    response = client.post(LOGOUT_ENDPOINT)

    assert response.status_code == 200
    assert response.json() == {"message": "Logout successful"}
