from fastapi.testclient import TestClient

from app.main import create_application

client = TestClient(create_application())


def test_health_check_returns_expected_response() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "sentinelai-backend",
        "version": "0.1.0",
        "environment": "development",
    }


def test_readiness_check_returns_ready_when_database_is_available() -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "database": "available",
    }
