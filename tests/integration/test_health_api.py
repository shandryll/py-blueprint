"""Integration tests for health endpoint."""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client() -> TestClient:
    """FastAPI test client."""
    return TestClient(app)


def test_health_returns_200_and_status(client: TestClient) -> None:
    """GET /api/v1/health/ returns 200 with status, version and timestamp."""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data
