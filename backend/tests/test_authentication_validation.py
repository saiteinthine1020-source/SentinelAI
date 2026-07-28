from fastapi.testclient import TestClient


def test_registration_rejects_missing_fields(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={},
    )

    assert response.status_code == 422


def test_registration_rejects_overlong_username(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "a" * 51,
            "email": "long.username@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 422


def test_registration_rejects_overlong_password(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "long_password_user",
            "email": "long.password@example.com",
            "password": "A1!" + ("a" * 126),
        },
    )

    assert response.status_code == 422


def test_login_rejects_missing_password(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "missing.password@example.com",
        },
    )

    assert response.status_code == 422


def test_login_rejects_non_json_body(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/auth/login",
        content="not-json",
        headers={
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 422
