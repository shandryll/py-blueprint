import pytest

from src.domain.entities.product import Product
from src.domain.exceptions.product_exceptions import ProductValidationError


def test_create_product_valid() -> None:
    product = Product.create(name="Valid Product", price=10.0, stock=5)
    assert product.name == "Valid Product"
    assert product.price == 10.0
    assert product.stock == 5


def test_create_product_empty_name_raises() -> None:
    with pytest.raises(ProductValidationError) as exc_info:
        Product.create(name="", price=10.0, stock=5)
    assert "empty" in str(exc_info.value.message).lower()


def test_create_product_whitespace_name_raises() -> None:
    with pytest.raises(ProductValidationError) as exc_info:
        Product.create(name="   ", price=10.0, stock=5)
    assert "empty" in str(exc_info.value.message).lower()


def test_create_product_zero_price_raises() -> None:
    with pytest.raises(ProductValidationError) as exc_info:
        Product.create(name="Product", price=0, stock=5)
    assert "price" in str(exc_info.value.message).lower()


def test_create_product_negative_price_raises() -> None:
    with pytest.raises(ProductValidationError) as exc_info:
        Product.create(name="Product", price=-1.0, stock=5)
    assert "price" in str(exc_info.value.message).lower()


def test_create_product_negative_stock_raises() -> None:
    with pytest.raises(ProductValidationError) as exc_info:
        Product.create(name="Product", price=10.0, stock=-1)
    assert "stock" in str(exc_info.value.message).lower()


def test_update_product_whitespace_name_raises() -> None:
    product = Product.create(name="Original", price=10.0, stock=5)
    with pytest.raises(ProductValidationError) as exc_info:
        product.update(name="   ")
    assert "empty" in str(exc_info.value.message).lower()


def test_product_update_preserves_fields_not_provided() -> None:
    product = Product.create(name="Original", price=10.0, stock=5, description="Desc")
    updated = product.update(price=20.0)
    assert updated.name == "Original"
    assert updated.price == 20.0
    assert updated.stock == 5
    assert updated.description == "Desc"
    assert updated.id == product.id
    assert updated.created_at == product.created_at
    assert updated.updated_at is not None
