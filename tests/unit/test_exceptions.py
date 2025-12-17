"""Testes para exceções."""

from src.core.exceptions import ApplicationServiceError


def test_application_service_error_initialization() -> None:
    """Testa a inicialização de ApplicationServiceError."""
    error = ApplicationServiceError(service_name="TestService", message="Test error")
    assert error.service_name == "TestService"
    assert error.message == "Test error"
    assert str(error) == "[TestService Service] - Test error"


def test_application_service_error_str_representation() -> None:
    """Testa a representação em string da exceção."""
    error = ApplicationServiceError(service_name="MyService", message="Something went wrong")
    assert "[MyService Service]" in str(error)
    assert "Something went wrong" in str(error)


def test_application_service_error_inherits_from_exception() -> None:
    """Testa que ApplicationServiceError herda de Exception."""
    error = ApplicationServiceError(service_name="Test", message="Error")
    assert isinstance(error, Exception)
