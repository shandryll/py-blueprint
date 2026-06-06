from fastapi.testclient import TestClient

from src.infrastructure.input.http.fastapi.main import create_app


def test_health_returns_200_and_status() -> None:
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data
