"""Unit tests for ApplicationServiceError (src.core.exceptions.application_errors)."""

from src.core.exceptions.application_errors import ApplicationServiceError


def test_application_service_error_str() -> None:
    """__str__ includes service name and message."""
    err = ApplicationServiceError(
        service_name="TestService",
        message="Something failed",
    )
    assert "TestService" in str(err)
    assert "Something failed" in str(err)


def test_application_service_error_defaults() -> None:
    """Default error_code and status_code are applied."""
    err = ApplicationServiceError(service_name="S", message="M")
    assert err.error_code == "APPLICATION_ERROR"
    assert err.status_code == 500


def test_application_service_error_custom_code_and_status() -> None:
    """Custom error_code and status_code are stored."""
    err = ApplicationServiceError(
        service_name="S",
        message="M",
        error_code="NOT_FOUND",
        status_code=404,
    )
    assert err.error_code == "NOT_FOUND"
    assert err.status_code == 404


def test_application_service_error_to_dict() -> None:
    """to_dict returns JSON-serializable structure for API."""
    err = ApplicationServiceError(
        service_name="ProductService",
        message="Product not found",
        error_code="PRODUCT_NOT_FOUND",
        status_code=404,
    )
    d = err.to_dict()
    assert d["service"] == "ProductService"
    assert d["message"] == "Product not found"
    assert d["error_code"] == "PRODUCT_NOT_FOUND"
    assert d["status_code"] == 404
    assert d["error"] == "Application Service Error"
