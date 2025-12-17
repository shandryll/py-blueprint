from fastapi.testclient import TestClient

from src.main import app


def test_health_endpoint() -> None:
    """Testa o endpoint de saúde."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data
