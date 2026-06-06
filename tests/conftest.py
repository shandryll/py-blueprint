import logging
import warnings

warnings.filterwarnings("ignore", message="Using `httpx` with `starlette.testclient` is deprecated")

import pytest
from fastapi.testclient import TestClient

from src.application.use_cases.product_use_case import ProductUseCase
from src.infrastructure.input.http.fastapi.main import create_app
from src.infrastructure.output.persistence.in_memory.product_repository import InMemoryProductRepository

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture
def sample_product_data() -> dict:
    return {
        "name": "Test Product",
        "description": "A test product",
        "price": 10.5,
        "stock": 5,
    }


@pytest.fixture
def in_memory_repository() -> InMemoryProductRepository:
    return InMemoryProductRepository()


@pytest.fixture
def product_use_case(in_memory_repository: InMemoryProductRepository) -> ProductUseCase:
    return ProductUseCase(in_memory_repository)
