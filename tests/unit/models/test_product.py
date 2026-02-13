"""Unit tests for product models (src.models.product)."""

import pytest
from pydantic import ValidationError

from src.models.product import ProductCreate, ProductUpdate


def test_product_create_valid() -> None:
    """ProductCreate accepts valid fields."""
    data = ProductCreate(
        name="Valid Product",
        description="Desc",
        price=1.0,
        stock=0,
    )
    assert data.name == "Valid Product"
    assert data.price == 1.0
    assert data.stock == 0


def test_product_create_name_stripped() -> None:
    """ProductCreate strips leading/trailing spaces from name."""
    data = ProductCreate(name="  Name  ", description=None, price=1.0, stock=0)
    assert data.name == "Name"


def test_product_create_name_whitespace_only_raises() -> None:
    """ProductCreate raises ValueError when name is only whitespace."""
    with pytest.raises(ValueError) as exc_info:
        ProductCreate(name="   ", description=None, price=1.0, stock=0)
    assert "cannot be only whitespace" in str(exc_info.value).lower()


def test_product_create_name_empty_raises() -> None:
    """ProductCreate raises ValidationError for empty name."""
    with pytest.raises(ValidationError):
        ProductCreate(name="", description=None, price=1.0, stock=0)


def test_product_create_price_positive() -> None:
    """ProductCreate requires price > 0."""
    with pytest.raises(ValidationError):
        ProductCreate(name="X", description=None, price=0, stock=0)
    with pytest.raises(ValidationError):
        ProductCreate(name="X", description=None, price=-1, stock=0)


def test_product_create_stock_non_negative() -> None:
    """ProductCreate requires stock >= 0."""
    with pytest.raises(ValidationError):
        ProductCreate(name="X", description=None, price=1.0, stock=-1)


def test_product_update_all_optional() -> None:
    """ProductUpdate has all optional fields."""
    data = ProductUpdate()
    assert data.name is None
    assert data.price is None
    assert data.stock is None


def test_product_update_partial() -> None:
    """ProductUpdate accepts partial updates."""
    data = ProductUpdate(name="New Name", price=2.0)
    assert data.name == "New Name"
    assert data.price == 2.0
    assert data.stock is None
