"""Unit tests for error decorators (src.core.exceptions.error_decorators)."""

from typing import NoReturn

import pytest
from pydantic import BaseModel

from src.core.exceptions import ApplicationServiceError
from src.core.exceptions.error_decorators import (
    handle_service_errors_async,
    handle_service_errors_sync,
)


@pytest.mark.asyncio
async def test_handle_service_errors_async_success() -> None:
    """Decorator returns result when no exception."""

    @handle_service_errors_async(service_name="Test", error_code="E1")
    async def ok() -> str:
        return "ok"

    result = await ok()
    assert result == "ok"


@pytest.mark.asyncio
async def test_handle_service_errors_async_application_error_reraised() -> None:
    """ApplicationServiceError is re-raised unchanged."""

    @handle_service_errors_async(service_name="Test", error_code="E1")
    async def fail() -> NoReturn:
        raise ApplicationServiceError(
            service_name="Test",
            message="Custom",
            error_code="CUSTOM",
            status_code=400,
        )

    with pytest.raises(ApplicationServiceError) as exc_info:
        await fail()
    assert exc_info.value.message == "Custom"
    assert exc_info.value.error_code == "CUSTOM"
    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_handle_service_errors_async_value_error_wrapped() -> None:
    """ValueError is wrapped in ApplicationServiceError."""

    @handle_service_errors_async(service_name="Test", error_code="V1")
    async def fail() -> NoReturn:
        raise ValueError("invalid value")

    with pytest.raises(ApplicationServiceError) as exc_info:
        await fail()
    assert exc_info.value.service_name == "Test"
    assert "invalid value" in exc_info.value.message
    assert exc_info.value.error_code == "V1"
    assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_handle_service_errors_async_validation_error_wrapped() -> None:
    """Pydantic ValidationError is wrapped with 422."""

    class RequiredField(BaseModel):
        required_field: str

    @handle_service_errors_async(service_name="Test", error_code="V2")
    async def fail() -> NoReturn:
        RequiredField()  # type: ignore[call-arg]

    with pytest.raises(ApplicationServiceError) as exc_info:
        await fail()
    assert exc_info.value.error_code == "VALIDATION_ERROR"
    assert exc_info.value.status_code == 422


def test_handle_service_errors_sync_success() -> None:
    """Sync decorator returns result when no exception."""

    @handle_service_errors_sync(service_name="Test", error_code="E1")
    def ok() -> str:
        return "sync_ok"

    assert ok() == "sync_ok"


def test_handle_service_errors_sync_generic_exception_wrapped() -> None:
    """Generic Exception is wrapped in ApplicationServiceError."""

    @handle_service_errors_sync(service_name="Test", error_code="E2")
    def fail() -> NoReturn:
        raise RuntimeError("runtime")

    with pytest.raises(ApplicationServiceError) as exc_info:
        fail()
    assert "fail" in exc_info.value.message
    assert exc_info.value.error_code == "E2"
    assert exc_info.value.status_code == 500
