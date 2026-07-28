from fastapi.testclient import TestClient


def test_registration_response_never_exposes_sensitive_fields(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "safe_response_user",
            "email": "safe.response@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 201

    body = response.json()

    forbidden_fields = {
        "password",
        "password_hash",
        "jwt",
        "token",
        "access_token",
        "cookie",
    }

    assert forbidden_fields.isdisjoint(body)


def test_login_response_never_exposes_token(
    client: TestClient,
) -> None:
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "safe_login_user",
            "email": "safe.login@example.com",
            "password": "StrongPassword123!",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "safe.login@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "token" not in body
    assert "access_token" not in body
    assert "jwt" not in body
    assert "cookie" not in body


def test_current_user_response_never_exposes_sensitive_fields(
    client: TestClient,
) -> None:
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "safe_me_user",
            "email": "safe.me@example.com",
            "password": "StrongPassword123!",
        },
    )

    client.post(
        "/api/v1/auth/login",
        json={
            "email": "safe.me@example.com",
            "password": "StrongPassword123!",
        },
    )

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 200

    body = response.json()

    forbidden_fields = {
        "password",
        "password_hash",
        "jwt",
        "token",
        "access_token",
        "cookie",
    }

    assert forbidden_fields.isdisjoint(body)
