"""Unit tests for FastAPI exception handlers (src.core.exceptions.fastapi_handlers)."""

from unittest.mock import MagicMock

import pytest
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.exceptions.application_errors import ApplicationServiceError
from src.core.exceptions.fastapi_handlers import (
    application_error_handler,
    http_exception_handler,
    validation_exception_handler,
)


@pytest.mark.asyncio
async def test_application_error_handler_returns_json() -> None:
    """application_error_handler returns JSONResponse with error body."""
    request = MagicMock()
    request.url.path = "/api/products"
    exc = ApplicationServiceError(
        service_name="ProductService",
        message="Product not found",
        error_code="PRODUCT_NOT_FOUND",
        status_code=404,
    )
    response = await application_error_handler(request, exc)
    assert response.status_code == 404
    body = response.body.decode()
    assert "Product not found" in body
    assert "PRODUCT_NOT_FOUND" in body
    assert "timestamp" in body
    assert "/api/products" in body


@pytest.mark.asyncio
async def test_http_exception_handler_404() -> None:
    """http_exception_handler returns JSON with NOT_FOUND for 404."""
    request = MagicMock()
    request.url.path = "/api/products/123"
    exc = StarletteHTTPException(status_code=404, detail="Not Found")
    response = await http_exception_handler(request, exc)
    assert response.status_code == 404
    body = response.body.decode()
    assert "NOT_FOUND" in body or "Not Found" in body


@pytest.mark.asyncio
async def test_validation_exception_handler_returns_422() -> None:
    """validation_exception_handler returns 422 with errors list."""
    request = MagicMock()
    request.url.path = "/api/products"

    class RequiredField(BaseModel):
        name: str

    try:
        RequiredField()
    except PydanticValidationError as e:
        exc = RequestValidationError(e.errors())
    else:
        pytest.skip("Could not create validation error")

    response = await validation_exception_handler(request, exc)
    assert response.status_code == 422
    body = response.body.decode()
    assert "VALIDATION_ERROR" in body
    assert "Validation" in body or "validation" in body
