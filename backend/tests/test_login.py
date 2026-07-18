from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User

LOGIN_ENDPOINT = "/api/v1/auth/login"


def create_user(
    db_session: Session,
    *,
    email: str = "login.user@example.com",
    password: str = "StrongPassword123!",
    is_active: bool = True,
) -> User:
    user = User(
        username="login_user",
        email=email,
        password_hash=hash_password(password),
        is_active=is_active,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def test_login_sets_http_only_cookie(
    client: TestClient,
    db_session: Session,
) -> None:
    create_user(db_session)

    response = client.post(
        LOGIN_ENDPOINT,
        json={
            "email": "LOGIN.USER@EXAMPLE.COM",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

    set_cookie = response.headers["set-cookie"]

    assert "sentinelai_access_token=" in set_cookie
    assert "HttpOnly" in set_cookie
    assert "Max-Age=1800" in set_cookie
    assert "Path=/" in set_cookie
    assert "SameSite=lax" in set_cookie

    assert "access_token" not in response.json()


def test_login_rejects_unknown_email(
    client: TestClient,
) -> None:
    response = client.post(
        LOGIN_ENDPOINT,
        json={
            "email": "unknown@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password"}


def test_login_rejects_wrong_password(
    client: TestClient,
    db_session: Session,
) -> None:
    create_user(db_session)

    response = client.post(
        LOGIN_ENDPOINT,
        json={
            "email": "login.user@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password"}


def test_login_rejects_inactive_user(
    client: TestClient,
    db_session: Session,
) -> None:
    create_user(
        db_session,
        email="inactive@example.com",
        is_active=False,
    )

    response = client.post(
        LOGIN_ENDPOINT,
        json={
            "email": "inactive@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Account access is disabled"}


def test_login_rejects_invalid_email_format(
    client: TestClient,
) -> None:
    response = client.post(
        LOGIN_ENDPOINT,
        json={
            "email": "not-an-email",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 422


def test_login_rejects_empty_password(
    client: TestClient,
) -> None:
    response = client.post(
        LOGIN_ENDPOINT,
        json={
            "email": "login.user@example.com",
            "password": "",
        },
    )

    assert response.status_code == 422
