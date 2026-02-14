import inspect
import logging
from contextvars import ContextVar

import structlog
from structlog.stdlib import LoggerFactory

from src.core.settings import get_settings

# Context variable para armazenar o correlation ID da requisição atual
_correlation_id_var: ContextVar[str | None] = ContextVar("correlation_id", default=None)


def get_correlation_id() -> str | None:
    """Obtém o correlation ID da requisição atual.

    Returns:
        str | None: O correlation ID ou None se não houver requisição ativa.
    """
    return _correlation_id_var.get()


def set_correlation_id(correlation_id: str) -> None:
    """Define o correlation ID para a requisição atual.

    Args:
        correlation_id: O ID único para rastrear a requisição.
    """
    _correlation_id_var.set(correlation_id)


def _add_correlation_id(logger: structlog.BoundLogger, method_name: str, event_dict: dict) -> dict:
    """Processor que adiciona correlation_id a todos os logs.

    Args:
        logger: Logger do structlog.
        method_name: Nome do método (debug, info, warning, error).
        event_dict: Dicionário de eventos.

    Returns:
        dict: Event dict atualizado com correlation_id se disponível.
    """
    correlation_id = get_correlation_id()
    if correlation_id:
        event_dict["correlation_id"] = correlation_id
    return event_dict


class _LoggingConfig:
    """Singleton para controlar configuração do logging."""

    _configured = False

    @classmethod
    def is_configured(cls) -> bool:
        """Verifica se já foi configurado."""
        return cls._configured

    @classmethod
    def mark_configured(cls) -> None:
        """Marca como configurado."""
        cls._configured = True


def _setup() -> None:
    """Configura structlog uma única vez."""
    if _LoggingConfig.is_configured():
        return

    settings = get_settings()

    # Processors para formatação (apenas o essencial)
    processors = [
        _add_correlation_id,  # Adiciona correlation_id do contexto
        structlog.stdlib.add_log_level,  # Adiciona nível do log
        structlog.processors.TimeStamper(fmt="iso"),  # Timestamp ISO
    ]

    # Escolhe renderer baseado na configuração
    if settings.log_format_json:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    # Configura structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    log_level = logging.DEBUG if settings.debug else getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(
        format="%(message)s",
        level=log_level,
    )

    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    _LoggingConfig.mark_configured()


class SimpleLogger:
    """Wrapper que mantém compatibilidade com a interface anterior."""

    def __init__(self, logger: structlog.BoundLogger) -> None:
        self._logger = logger

    def debug(self, message: str, **kwargs: object) -> None:
        """Log de debug.

        Args:
            message: Mensagem do log.
            **kwargs: Dados extras para incluir no log.
        """
        self._logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs: object) -> None:
        """Log de info.

        Args:
            message: Mensagem do log.
            **kwargs: Dados extras para incluir no log.
        """
        self._logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs: object) -> None:
        """Log de warning.

        Args:
            message: Mensagem do log.
            **kwargs: Dados extras para incluir no log.
        """
        self._logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs: object) -> None:
        """Log de error.

        Args:
            message: Mensagem do log.
            **kwargs: Dados extras para incluir no log.
        """
        self._logger.error(message, **kwargs, exc_info=True)


def get_logger(name: str | None = None) -> SimpleLogger:
    """Obtém um logger configurado.

    Args:
        name: Nome do logger (geralmente __name__). Se None, detecta automaticamente.

    Returns:
        SimpleLogger: Logger configurado.

    Examples:
        logger = get_logger(__name__)
        # Adicionar dados extras diretamente no log
        logger.info("Product created", product_id="123", price=99.90, category="electronics")
        logger.error("Error processing", user_id="456", operation="create", error_code="E001")
        logger.debug("Validando dados", count=10, status="processing")
    """
    _setup()

    if name is None:
        frame = inspect.currentframe()
        name = frame.f_back.f_globals.get("__name__", "unknown") if frame and frame.f_back else "unknown"

    logger = structlog.get_logger(name)
    return SimpleLogger(logger)
