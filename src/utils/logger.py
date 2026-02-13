import inspect
import logging

import structlog
from structlog.stdlib import LoggerFactory

from src.core.settings import get_settings


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

    # Reduz ruído do uvicorn
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
