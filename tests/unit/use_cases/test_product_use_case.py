from uuid import uuid4

import pytest

from src.application.use_cases.product_use_case import ProductUseCase
from src.domain.exceptions.product_exceptions import (
    ProductNameAlreadyExistsError,
    ProductNotFoundError,
)
from src.infrastructure.output.persistence.in_memory.product_repository import InMemoryProductRepository


@pytest.fixture
def use_case() -> ProductUseCase:
    return ProductUseCase(InMemoryProductRepository())


@pytest.mark.asyncio
async def test_create_product_success(use_case: ProductUseCase) -> None:
    out = await use_case.create_product(name="NewProduct", price=10.0, stock=5, description="D")
    assert out.name == "NewProduct"
    assert out.id is not None
    assert out.price == 10.0


@pytest.mark.asyncio
async def test_create_product_duplicate_name_raises(use_case: ProductUseCase) -> None:
    await use_case.create_product(name="SameName", price=1.0, stock=0)
    with pytest.raises(ProductNameAlreadyExistsError) as exc_info:
        await use_case.create_product(name="SameName", price=1.0, stock=0)
    assert exc_info.value.code == "PRODUCT_NAME_ALREADY_EXISTS"


@pytest.mark.asyncio
async def test_get_by_id_found(use_case: ProductUseCase) -> None:
    created = await use_case.create_product(name="G1", price=1.0, stock=0)
    found = await use_case.get_product_by_id(created.id)
    assert found.id == created.id
    assert found.name == "G1"


@pytest.mark.asyncio
async def test_get_by_id_not_found_raises(use_case: ProductUseCase) -> None:
    with pytest.raises(ProductNotFoundError) as exc_info:
        await use_case.get_product_by_id(uuid4())
    assert exc_info.value.code == "PRODUCT_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_by_name_found(use_case: ProductUseCase) -> None:
    created = await use_case.create_product(name="ByName", price=1.0, stock=0)
    found = await use_case.get_product_by_name("ByName")
    assert found.id == created.id


@pytest.mark.asyncio
async def test_get_by_name_not_found_raises(use_case: ProductUseCase) -> None:
    with pytest.raises(ProductNotFoundError) as exc_info:
        await use_case.get_product_by_name("Nonexistent")
    assert exc_info.value.code == "PRODUCT_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_all_products(use_case: ProductUseCase) -> None:
    for name in ["A", "B"]:
        await use_case.create_product(name=name, price=1.0, stock=0)
    all_products = await use_case.get_all_products(skip=0, limit=10)
    assert len(all_products) == 2
    names = {p.name for p in all_products}
    assert names == {"A", "B"}


@pytest.mark.asyncio
async def test_update_product_success(use_case: ProductUseCase) -> None:
    created = await use_case.create_product(name="Original", price=1.0, stock=0)
    updated = await use_case.update_product(
        product_id=created.id,
        name="Updated",
        price=2.0,
        stock=1,
    )
    assert updated.name == "Updated"
    assert updated.price == 2.0


@pytest.mark.asyncio
async def test_update_product_not_found_raises(use_case: ProductUseCase) -> None:
    with pytest.raises(ProductNotFoundError) as exc_info:
        await use_case.update_product(uuid4(), name="X", price=1.0)
    assert exc_info.value.code == "PRODUCT_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_product_duplicate_name_raises(use_case: ProductUseCase) -> None:
    await use_case.create_product(name="First", price=1.0, stock=0)
    second = await use_case.create_product(name="Second", price=1.0, stock=0)

    with pytest.raises(ProductNameAlreadyExistsError) as exc_info:
        await use_case.update_product(second.id, name="First", price=1.0, stock=1)
    assert exc_info.value.code == "PRODUCT_NAME_ALREADY_EXISTS"


@pytest.mark.asyncio
async def test_delete_product_success(use_case: ProductUseCase) -> None:
    created = await use_case.create_product(name="ToDelete", price=1.0, stock=0)
    await use_case.delete_product(created.id)
    with pytest.raises(ProductNotFoundError):
        await use_case.get_product_by_id(created.id)


@pytest.mark.asyncio
async def test_delete_product_not_found_raises(use_case: ProductUseCase) -> None:
    with pytest.raises(ProductNotFoundError) as exc_info:
        await use_case.delete_product(uuid4())
    assert exc_info.value.code == "PRODUCT_NOT_FOUND"
