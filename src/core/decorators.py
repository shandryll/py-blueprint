import traceback
from collections.abc import Callable
from functools import wraps
from typing import TypeVar

from src.core.exceptions import ApplicationServiceError

T = TypeVar("T")


def handle_application_service_error(service_name: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Trata exceções e converte para ApplicationServiceError.

    Args:
        service_name: Nome do serviço para incluir na exceção.

    Returns:
        Decorator que envolve a função com tratamento de exceções.

    Note:
        - Não captura ApplicationServiceError (evita duplo encapsulamento)
        - Não captura KeyboardInterrupt e SystemExit
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: object, **kwargs: object) -> T:
            try:
                return func(*args, **kwargs)
            except ApplicationServiceError:
                raise
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as err:
                raise ApplicationServiceError(
                    service_name=service_name,
                    message=traceback.format_exc(),
                ) from err

        return wrapper

    return decorator
