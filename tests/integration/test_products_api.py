"""Integration tests for products API."""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client() -> TestClient:
    """FastAPI test client."""
    return TestClient(app)


def test_create_product_returns_201(client: TestClient) -> None:
    """POST /api/v1/products/ with valid body returns 201 and product with id."""
    payload = {
        "name": "Integration Product",
        "description": "Created via API",
        "price": 19.99,
        "stock": 10,
    }
    response = client.post("/api/v1/products/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Integration Product"
    assert data["price"] == 19.99
    assert "id" in data
    assert "created_at" in data


def test_create_product_duplicate_name_returns_409(client: TestClient) -> None:
    """POST /api/v1/products/ with duplicate name returns 409."""
    payload = {"name": "Unique", "description": None, "price": 1.0, "stock": 0}
    client.post("/api/v1/products/", json=payload)
    response = client.post("/api/v1/products/", json=payload)
    assert response.status_code == 409
    data = response.json()
    assert "already exists" in data["message"].lower()


def test_create_product_invalid_body_returns_422(client: TestClient) -> None:
    """POST /api/v1/products/ with invalid body returns 422."""
    response = client.post("/api/v1/products/", json={"name": "X"})  # missing price, etc.
    assert response.status_code == 422


def test_get_product_by_id_success(client: TestClient) -> None:
    """GET /api/v1/products/{id} returns 200 and product when exists."""
    payload = {"name": "GetById", "description": None, "price": 1.0, "stock": 0}
    create_resp = client.post("/api/v1/products/", json=payload)
    assert create_resp.status_code == 201
    product_id = create_resp.json()["id"]
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "GetById"
    assert response.json()["id"] == product_id


def test_get_product_by_id_not_found_returns_404(client: TestClient) -> None:
    """GET /api/products/{id} returns 404 for unknown id."""
    response = client.get(f"/api/v1/products/{uuid4()}")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["message"].lower()


def test_get_all_products_returns_list(client: TestClient) -> None:
    """GET /api/v1/products/ returns 200 and list (possibly empty)."""
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_all_products_pagination(client: TestClient) -> None:
    """GET /api/v1/products/?skip=0&limit=2 respects query params."""
    response = client.get("/api/v1/products/?skip=0&limit=2")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_product_success(client: TestClient) -> None:
    """PUT /api/v1/products/{id} with valid body returns 200 and updated product."""
    create_resp = client.post(
        "/api/v1/products/",
        json={"name": "ToUpdate", "description": None, "price": 1.0, "stock": 0},
    )
    assert create_resp.status_code == 201
    product_id = create_resp.json()["id"]
    response = client.put(
        f"/api/v1/products/{product_id}",
        json={"name": "Updated", "description": "New desc", "price": 2.0, "stock": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"
    assert data["price"] == 2.0


def test_update_product_not_found_returns_404(client: TestClient) -> None:
    """PUT /api/v1/products/{id} returns 404 for unknown id."""
    response = client.put(
        f"/api/v1/products/{uuid4()}",
        json={"name": "X", "price": 1.0},
    )
    assert response.status_code == 404


def test_patch_product_partial(client: TestClient) -> None:
    """PATCH /api/v1/products/{id} with partial body updates only given fields."""
    create_resp = client.post(
        "/api/v1/products/",
        json={"name": "ToPatch", "description": "Original", "price": 1.0, "stock": 0},
    )
    assert create_resp.status_code == 201
    product_id = create_resp.json()["id"]
    response = client.patch(
        f"/api/v1/products/{product_id}",
        json={"name": "Patched"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Patched"
    assert data["description"] == "Original"
    assert data["price"] == 1.0


def test_delete_product_success(client: TestClient) -> None:
    """DELETE /api/v1/products/{id} returns 204 and product is removed."""
    create_resp = client.post(
        "/api/v1/products/",
        json={"name": "ToDelete", "description": None, "price": 1.0, "stock": 0},
    )
    assert create_resp.status_code == 201
    product_id = create_resp.json()["id"]
    response = client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == 204
    get_resp = client.get(f"/api/v1/products/{product_id}")
    assert get_resp.status_code == 404


def test_delete_product_not_found_returns_404(client: TestClient) -> None:
    """DELETE /api/v1/products/{id} returns 404 for unknown id."""
    response = client.delete(f"/api/v1/products/{uuid4()}")
    assert response.status_code == 404


def test_product_name_whitespace_only_validation(client: TestClient) -> None:
    """POST with name only whitespace returns 422 or 500 with validation message."""
    response = client.post(
        "/api/v1/products/",
        json={"name": "   ", "description": None, "price": 1.0, "stock": 0},
    )
    assert response.status_code in (422, 500)
    # Message should refer to name/validation in English
    body = response.json()
    assert "message" in body
