"""Unit tests for InMemoryProductRepository (src.repositories.in_memory.in_memory_product_repository)."""

from uuid import uuid4

import pytest

from src.models.product import ProductCreate, ProductResponse, ProductUpdate
from src.repositories.in_memory import InMemoryProductRepository


@pytest.fixture
def repo() -> InMemoryProductRepository:
    """Fresh in-memory repository."""
    return InMemoryProductRepository()


@pytest.mark.asyncio
async def test_create_returns_product(repo: InMemoryProductRepository) -> None:
    """Create stores and returns a ProductResponse with id and timestamps."""
    data = ProductCreate(name="P1", description="D1", price=1.0, stock=1)
    out = await repo.create(data)
    assert isinstance(out, ProductResponse)
    assert out.id is not None
    assert out.name == "P1"
    assert out.price == 1.0
    assert out.created_at is not None
    assert out.updated_at is None


@pytest.mark.asyncio
async def test_get_by_id_found(repo: InMemoryProductRepository) -> None:
    """Get_by_id returns the product when it exists."""
    data = ProductCreate(name="P1", description=None, price=1.0, stock=0)
    created = await repo.create(data)
    found = await repo.get_by_id(created.id)
    assert found is not None
    assert found.id == created.id
    assert found.name == "P1"


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo: InMemoryProductRepository) -> None:
    """Get_by_id returns None when product does not exist."""
    found = await repo.get_by_id(uuid4())
    assert found is None


@pytest.mark.asyncio
async def test_get_by_name_found(repo: InMemoryProductRepository) -> None:
    """Get_by_name finds product case-insensitively."""
    data = ProductCreate(name="UniqueName", description=None, price=1.0, stock=0)
    created = await repo.create(data)
    found = await repo.get_by_name("uniquename")
    assert found is not None
    assert found.id == created.id


@pytest.mark.asyncio
async def test_get_by_name_not_found(repo: InMemoryProductRepository) -> None:
    """Get_by_name returns None when product does not exist."""
    found = await repo.get_by_name("Nonexistent")
    assert found is None


@pytest.mark.asyncio
async def test_get_all_pagination(repo: InMemoryProductRepository) -> None:
    """Get_all respects skip and limit."""
    for i in range(5):
        await repo.create(ProductCreate(name=f"P{i}", description=None, price=float(i + 1), stock=0))
    page = await repo.get_all(skip=1, limit=2)
    assert len(page) == 2
    assert page[0].name == "P1"
    assert page[1].name == "P2"


@pytest.mark.asyncio
async def test_update_existing(repo: InMemoryProductRepository) -> None:
    """Update modifies and returns the product."""
    created = await repo.create(ProductCreate(name="Old", description=None, price=1.0, stock=0))
    update = ProductUpdate(name="New", price=2.0)
    updated = await repo.update(created.id, update)
    assert updated is not None
    assert updated.name == "New"
    assert updated.price == 2.0
    assert updated.updated_at is not None


@pytest.mark.asyncio
async def test_update_not_found(repo: InMemoryProductRepository) -> None:
    """Update returns None when product does not exist."""
    update = ProductUpdate(name="X", price=1.0)
    result = await repo.update(uuid4(), update)
    assert result is None


@pytest.mark.asyncio
async def test_delete_existing(repo: InMemoryProductRepository) -> None:
    """Delete removes the product and returns True."""
    created = await repo.create(ProductCreate(name="ToDelete", description=None, price=1.0, stock=0))
    deleted = await repo.delete(created.id)
    assert deleted is True
    assert await repo.get_by_id(created.id) is None


@pytest.mark.asyncio
async def test_delete_not_found(repo: InMemoryProductRepository) -> None:
    """Delete returns False when product does not exist."""
    deleted = await repo.delete(uuid4())
    assert deleted is False
