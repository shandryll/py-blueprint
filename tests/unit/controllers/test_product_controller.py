"""Unit tests for ProductController (src.controllers.product_controller)."""

from uuid import uuid4

import pytest

from src.controllers.product_controller import ProductController
from src.core.exceptions import ApplicationServiceError
from src.models.product import ProductCreate, ProductUpdate
from src.repositories.in_memory import InMemoryProductRepository
from src.services.product_service import ProductService


@pytest.fixture
def controller() -> ProductController:
    """ProductController with in-memory service."""
    repo = InMemoryProductRepository()
    service = ProductService(repo)
    return ProductController(service)


@pytest.mark.asyncio
async def test_controller_create(controller: ProductController) -> None:
    """Controller create delegates to service and returns product."""
    data = ProductCreate(name="Ctrl", description=None, price=1.0, stock=0)
    out = await controller.create(data)
    assert out.name == "Ctrl"
    assert out.id is not None


@pytest.mark.asyncio
async def test_controller_get_by_id(controller: ProductController) -> None:
    """Controller get_by_id returns product from service."""
    data = ProductCreate(name="GetById", description=None, price=1.0, stock=0)
    created = await controller.create(data)
    found = await controller.get_by_id(created.id)
    assert found.id == created.id
    assert found.name == "GetById"


@pytest.mark.asyncio
async def test_controller_get_by_id_not_found(controller: ProductController) -> None:
    """Controller get_by_id raises when product not found."""
    with pytest.raises(ApplicationServiceError):
        await controller.get_by_id(uuid4())


@pytest.mark.asyncio
async def test_controller_get_all(controller: ProductController) -> None:
    """Controller get_all returns list from service."""
    await controller.create(ProductCreate(name="A", description=None, price=1.0, stock=0))
    await controller.create(ProductCreate(name="B", description=None, price=1.0, stock=0))
    all_products = await controller.get_all(skip=0, limit=10)
    assert len(all_products) == 2


@pytest.mark.asyncio
async def test_controller_update(controller: ProductController) -> None:
    """Controller update delegates to service."""
    created = await controller.create(ProductCreate(name="Old", description=None, price=1.0, stock=0))
    updated = await controller.update(created.id, ProductUpdate(name="New", price=2.0))
    assert updated.name == "New"
    assert updated.price == 2.0


@pytest.mark.asyncio
async def test_controller_delete(controller: ProductController) -> None:
    """Controller delete removes product via service."""
    created = await controller.create(ProductCreate(name="Del", description=None, price=1.0, stock=0))
    await controller.delete(created.id)
    with pytest.raises(ApplicationServiceError):
        await controller.get_by_id(created.id)
