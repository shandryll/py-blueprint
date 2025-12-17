"""Testes para decorators."""

from src.core.decorators import handle_application_service_error
from src.core.exceptions import ApplicationServiceError


def test_decorator_preserves_successful_execution() -> None:
    """Testa que o decorator preserva execução bem-sucedida."""

    @handle_application_service_error("TestService")
    def successful_function() -> str:
        return "success"

    result = successful_function()
    assert result == "success"


def test_decorator_converts_generic_exception() -> None:
    """Testa que o decorator converte exceções genéricas."""

    @handle_application_service_error("TestService")
    def failing_function() -> None:
        raise ValueError("Original error")

    try:
        failing_function()
        raise AssertionError("Should have raised ApplicationServiceError")
    except ApplicationServiceError as e:
        assert e.service_name == "TestService"
        assert "Original error" in e.message or "ValueError" in e.message


def test_decorator_preserves_application_service_error() -> None:
    """Testa que o decorator não encapsula ApplicationServiceError."""

    @handle_application_service_error("TestService")
    def raises_app_error() -> None:
        raise ApplicationServiceError(service_name="OriginalService", message="Original error")

    try:
        raises_app_error()
        raise AssertionError("Should have raised ApplicationServiceError")
    except ApplicationServiceError as e:
        # Deve manter o erro original, não encapsular
        assert e.service_name == "OriginalService"
        assert e.message == "Original error"


def test_decorator_preserves_keyboard_interrupt() -> None:
    """Testa que o decorator não captura KeyboardInterrupt."""

    @handle_application_service_error("TestService")
    def raises_keyboard_interrupt() -> None:
        raise KeyboardInterrupt()

    try:
        raises_keyboard_interrupt()
        raise AssertionError("Should have raised KeyboardInterrupt")
    except KeyboardInterrupt:
        # Deve passar KeyboardInterrupt sem modificar
        pass
    except ApplicationServiceError:
        raise AssertionError("Should not have converted KeyboardInterrupt") from None


def test_decorator_preserves_system_exit() -> None:
    """Testa que o decorator não captura SystemExit."""

    @handle_application_service_error("TestService")
    def raises_system_exit() -> None:
        raise SystemExit()

    try:
        raises_system_exit()
        raise AssertionError("Should have raised SystemExit")
    except SystemExit:
        # Deve passar SystemExit sem modificar
        pass
    except ApplicationServiceError:
        raise AssertionError("Should not have converted SystemExit") from None
