from collections.abc import Awaitable, Callable
from functools import wraps
from typing import NoReturn, ParamSpec, TypeVar

from pydantic import ValidationError

from src.core.exceptions.application_errors import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
    ApplicationServiceError,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar("T")
P = ParamSpec("P")


def _handle_error(
    func_name: str,
    service_name: str,
    error_code: str,
    err: Exception,
) -> NoReturn:
    """Função auxiliar compartilhada para tratamento de erros.

    Args:
        func_name: Nome da função que gerou o erro.
        service_name: Nome do serviço para mensagens de erro.
        error_code: Código de erro padrão.
        err: Exceção capturada.

    Raises:
        ApplicationServiceError: Sempre lança ApplicationServiceError.
    """
    if isinstance(err, ApplicationServiceError):
        logger.error(
            "Service error",
            operation="error_handling",
            function=func_name,
            service=service_name,
            error_type="ApplicationServiceError",
            error_code=err.error_code,
            error_message=err.message,
            status_code=err.status_code,
        )
        raise err
    elif isinstance(err, ValidationError):
        logger.error(
            "Pydantic validation error",
            operation="error_handling",
            function=func_name,
            service=service_name,
            error_type="ValidationError",
            error_code="VALIDATION_ERROR",
            error_message=str(err),
        )
        raise ApplicationServiceError(
            service_name=service_name,
            message=f"Validation error: {str(err)}",
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
        ) from err
    elif isinstance(err, ValueError):
        logger.error(
            "Validation error",
            operation="error_handling",
            function=func_name,
            service=service_name,
            error_type="ValueError",
            error_code=error_code,
            error_message=str(err),
        )
        raise ApplicationServiceError(
            service_name=service_name,
            message=f"Validation error in {func_name}: {str(err)}",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=error_code,
        ) from err
    else:
        logger.error(
            "Unexpected error",
            operation="error_handling",
            function=func_name,
            service=service_name,
            error_type=type(err).__name__,
            error_code=error_code,
            error_message=str(err),
        )
        raise ApplicationServiceError(
            service_name=service_name,
            message=f"Error in {func_name}: {str(err)}",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=error_code,
        ) from err


def handle_service_errors_async(
    service_name: str,
    error_code: str = "SERVICE_ERROR",
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    """Trata erros padronizados nos métodos assíncronos do serviço.

    Args:
        service_name: Nome do serviço para mensagens de erro.
        error_code: Código de erro padrão caso ocorra exceção não tratada.

    Returns:
        Callable: Decorator que envolve o método assíncrono com tratamento de erros.

    Exemplo:
        @handle_service_errors_async(service_name="ProductService", error_code="CREATE_ERROR")
        async def create_product(self, data: ProductCreate) -> ProductResponse:
            # código do método
            pass
    """

    def decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except Exception as err:
                _handle_error(
                    func_name=func.__name__,
                    service_name=service_name,
                    error_code=error_code,
                    err=err,
                )

        return wrapper

    return decorator


def handle_service_errors_sync(
    service_name: str,
    error_code: str = "SERVICE_ERROR",
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Trata erros padronizados nos métodos síncronos do serviço.

    Args:
        service_name: Nome do serviço para mensagens de erro.
        error_code: Código de erro padrão caso ocorra exceção não tratada.

    Returns:
        Callable: Decorator que envolve o método síncrono com tratamento de erros.

    Exemplo:
        @handle_service_errors_sync(service_name="ProductService", error_code="VALIDATE_ERROR")
        def validate_product(self, data: ProductCreate) -> bool:
            # código do método
            pass
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as err:
                _handle_error(
                    func_name=func.__name__,
                    service_name=service_name,
                    error_code=error_code,
                    err=err,
                )

        return wrapper

    return decorator
