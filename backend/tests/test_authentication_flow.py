from fastapi.testclient import TestClient

REGISTER_ENDPOINT = "/api/v1/auth/register"
LOGIN_ENDPOINT = "/api/v1/auth/login"
ME_ENDPOINT = "/api/v1/auth/me"
LOGOUT_ENDPOINT = "/api/v1/auth/logout"


def test_complete_authentication_flow(
    client: TestClient,
) -> None:
    registration_response = client.post(
        REGISTER_ENDPOINT,
        json={
            "username": "flow_user",
            "email": "flow.user@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert registration_response.status_code == 201
    assert registration_response.json()["username"] == "flow_user"

    unauthenticated_response = client.get(ME_ENDPOINT)

    assert unauthenticated_response.status_code == 401

    login_response = client.post(
        LOGIN_ENDPOINT,
        json={
            "email": "flow.user@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200
    assert login_response.json() == {"message": "Login successful"}

    cookie_header = login_response.headers["set-cookie"]

    assert "sentinelai_access_token=" in cookie_header
    assert "HttpOnly" in cookie_header

    current_user_response = client.get(ME_ENDPOINT)

    assert current_user_response.status_code == 200

    current_user = current_user_response.json()

    assert current_user["username"] == "flow_user"
    assert current_user["email"] == "flow.user@example.com"
    assert current_user["is_active"] is True
    assert "password" not in current_user
    assert "password_hash" not in current_user

    logout_response = client.post(LOGOUT_ENDPOINT)

    assert logout_response.status_code == 200
    assert logout_response.json() == {"message": "Logout successful"}

    after_logout_response = client.get(ME_ENDPOINT)

    assert after_logout_response.status_code == 401
