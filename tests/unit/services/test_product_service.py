"""Unit tests for ProductService (src.services.product_service)."""

from uuid import uuid4

import pytest

from src.core.exceptions import ApplicationServiceError
from src.models.product import ProductCreate, ProductUpdate
from src.repositories.in_memory import InMemoryProductRepository
from src.services.product_service import ProductService


@pytest.fixture
def service() -> ProductService:
    """ProductService with fresh in-memory repository."""
    return ProductService(InMemoryProductRepository())


@pytest.mark.asyncio
async def test_create_product_success(service: ProductService) -> None:
    """Create product returns stored product with id."""
    data = ProductCreate(name="NewProduct", description="D", price=10.0, stock=5)
    out = await service.create_product(data)
    assert out.name == "NewProduct"
    assert out.id is not None
    assert out.price == 10.0


@pytest.mark.asyncio
async def test_create_product_duplicate_name_raises(service: ProductService) -> None:
    """Create product with existing name raises ApplicationServiceError 409."""
    data = ProductCreate(name="SameName", description=None, price=1.0, stock=0)
    await service.create_product(data)
    with pytest.raises(ApplicationServiceError) as exc_info:
        await service.create_product(data)
    assert exc_info.value.status_code == 409
    assert "already exists" in exc_info.value.message.lower()
    assert exc_info.value.error_code == "PRODUCT_NAME_ALREADY_EXISTS"


@pytest.mark.asyncio
async def test_get_by_id_found(service: ProductService) -> None:
    """Get_product_by_id returns product when it exists."""
    data = ProductCreate(name="G1", description=None, price=1.0, stock=0)
    created = await service.create_product(data)
    found = await service.get_product_by_id(created.id)
    assert found.id == created.id
    assert found.name == "G1"


@pytest.mark.asyncio
async def test_get_by_id_not_found_raises(service: ProductService) -> None:
    """Get_product_by_id raises ApplicationServiceError 404 when not found."""
    with pytest.raises(ApplicationServiceError) as exc_info:
        await service.get_product_by_id(uuid4())
    assert exc_info.value.status_code == 404
    assert "not found" in exc_info.value.message.lower()
    assert exc_info.value.error_code == "PRODUCT_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_by_name_found(service: ProductService) -> None:
    """Get_product_by_name returns product when it exists."""
    data = ProductCreate(name="ByName", description=None, price=1.0, stock=0)
    created = await service.create_product(data)
    found = await service.get_product_by_name("ByName")
    assert found.id == created.id


@pytest.mark.asyncio
async def test_get_by_name_not_found_raises(service: ProductService) -> None:
    """Get_product_by_name raises ApplicationServiceError 404 when not found."""
    with pytest.raises(ApplicationServiceError) as exc_info:
        await service.get_product_by_name("Nonexistent")
    assert exc_info.value.status_code == 404
    assert exc_info.value.error_code == "PRODUCT_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_all_products(service: ProductService) -> None:
    """Get_all_products returns list with pagination."""
    await service.create_product(ProductCreate(name="A", description=None, price=1.0, stock=0))
    await service.create_product(ProductCreate(name="B", description=None, price=2.0, stock=0))
    all_products = await service.get_all_products(skip=0, limit=10)
    assert len(all_products) == 2
    names = {p.name for p in all_products}
    assert names == {"A", "B"}


@pytest.mark.asyncio
async def test_update_product_success(service: ProductService) -> None:
    """Update_product modifies and returns product."""
    created = await service.create_product(ProductCreate(name="Original", description=None, price=1.0, stock=0))
    update = ProductUpdate(name="Updated", price=2.0, description=None, stock=1)
    updated = await service.update_product(created.id, update)
    assert updated.name == "Updated"
    assert updated.price == 2.0


@pytest.mark.asyncio
async def test_update_product_not_found_raises(service: ProductService) -> None:
    """Update_product raises 404 when product does not exist."""
    update = ProductUpdate(name="X", price=1.0, description=None, stock=1)
    with pytest.raises(ApplicationServiceError) as exc_info:
        await service.update_product(uuid4(), update)
    assert exc_info.value.status_code == 404
    assert exc_info.value.error_code == "PRODUCT_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_product_duplicate_name_raises(service: ProductService) -> None:
    """Update_product raises 409 when new name is taken by another product."""
    await service.create_product(ProductCreate(name="First", description=None, price=1.0, stock=0))
    second = await service.create_product(ProductCreate(name="Second", description=None, price=1.0, stock=0))
    with pytest.raises(ApplicationServiceError) as exc_info:
        await service.update_product(second.id, ProductUpdate(name="First", description=None, price=1.0, stock=1))
    assert exc_info.value.status_code == 409
    assert exc_info.value.error_code == "PRODUCT_NAME_ALREADY_EXISTS"


@pytest.mark.asyncio
async def test_delete_product_success(service: ProductService) -> None:
    """Delete_product removes the product."""
    created = await service.create_product(ProductCreate(name="ToDelete", description=None, price=1.0, stock=0))
    await service.delete_product(created.id)
    with pytest.raises(ApplicationServiceError):
        await service.get_product_by_id(created.id)


@pytest.mark.asyncio
async def test_delete_product_not_found_raises(service: ProductService) -> None:
    """Delete_product raises 404 when product does not exist."""
    with pytest.raises(ApplicationServiceError) as exc_info:
        await service.delete_product(uuid4())
    assert exc_info.value.status_code == 404
    assert exc_info.value.error_code == "PRODUCT_NOT_FOUND"
