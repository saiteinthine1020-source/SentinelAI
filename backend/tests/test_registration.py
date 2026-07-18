from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.user import User

REGISTER_ENDPOINT = "/api/v1/auth/register"


def valid_registration_payload() -> dict[str, str]:
    return {
        "username": "Sai_User",
        "email": "Sai.Example@Example.com",
        "password": "StrongPassword123!",
    }


def test_registration_creates_user(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        REGISTER_ENDPOINT,
        json=valid_registration_payload(),
    )

    assert response.status_code == 201

    body = response.json()

    assert body["username"] == "sai_user"
    assert body["email"] == "sai.example@example.com"
    assert body["is_active"] is True
    assert "id" in body
    assert "created_at" in body
    assert "password" not in body
    assert "password_hash" not in body

    user = db_session.scalar(
        select(User).where(
            User.email == "sai.example@example.com",
        )
    )

    assert user is not None
    assert user.password_hash != "StrongPassword123!"
    assert verify_password(
        "StrongPassword123!",
        user.password_hash,
    )


def test_registration_rejects_duplicate_email(
    client: TestClient,
) -> None:
    payload = valid_registration_payload()

    first_response = client.post(
        REGISTER_ENDPOINT,
        json=payload,
    )

    duplicate_response = client.post(
        REGISTER_ENDPOINT,
        json={
            **payload,
            "username": "different_username",
        },
    )

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409
    assert duplicate_response.json() == {"detail": "An account with this email already exists"}


def test_registration_rejects_duplicate_username(
    client: TestClient,
) -> None:
    payload = valid_registration_payload()

    first_response = client.post(
        REGISTER_ENDPOINT,
        json=payload,
    )

    duplicate_response = client.post(
        REGISTER_ENDPOINT,
        json={
            **payload,
            "email": "different@example.com",
        },
    )

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409
    assert duplicate_response.json() == {"detail": "This username is already in use"}


def test_registration_rejects_weak_password(
    client: TestClient,
) -> None:
    response = client.post(
        REGISTER_ENDPOINT,
        json={
            "username": "sai_user",
            "email": "sai@example.com",
            "password": "weakpassword",
        },
    )

    assert response.status_code == 422


def test_registration_rejects_invalid_username(
    client: TestClient,
) -> None:
    response = client.post(
        REGISTER_ENDPOINT,
        json={
            "username": "invalid username",
            "email": "sai@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 422


def test_registration_rejects_invalid_email(
    client: TestClient,
) -> None:
    response = client.post(
        REGISTER_ENDPOINT,
        json={
            "username": "sai_user",
            "email": "not-an-email",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 422
