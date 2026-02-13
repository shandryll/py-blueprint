"""Pytest configuration and shared fixtures."""

import logging

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.models.product import ProductCreate, ProductResponse
from src.repositories.in_memory import InMemoryProductRepository
from src.services.product_service import ProductService

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


@pytest.fixture
def client() -> TestClient:
    """FastAPI test client for integration tests."""
    return TestClient(app)


@pytest.fixture
def sample_product_data() -> dict:
    """Minimal valid product payload for API/create."""
    return {
        "name": "Test Product",
        "description": "A test product",
        "price": 10.5,
        "stock": 5,
    }


@pytest.fixture
def product_create(sample_product_data: dict) -> ProductCreate:
    """ProductCreate model instance."""
    return ProductCreate(**sample_product_data)


@pytest.fixture
def in_memory_repository() -> InMemoryProductRepository:
    """Fresh in-memory repository (no shared state)."""
    return InMemoryProductRepository()


@pytest.fixture
def product_service(in_memory_repository: InMemoryProductRepository) -> ProductService:
    """ProductService with in-memory repository."""
    return ProductService(in_memory_repository)


@pytest.fixture
async def created_product(
    product_service: ProductService,
    product_create: ProductCreate,
) -> ProductResponse:
    """One product already created in the service."""
    return await product_service.create_product(product_create)


@pytest.fixture
def product_id(created_product: ProductResponse):
    """UUID of the fixture-created product."""
    return created_product.id
