import logging
from contextvars import ContextVar

import structlog
from structlog.stdlib import LoggerFactory

from src.shared.settings import get_settings

_correlation_id_var: ContextVar[str | None] = ContextVar("correlation_id", default=None)


def get_correlation_id() -> str | None:
    return _correlation_id_var.get()


def set_correlation_id(correlation_id: str) -> None:
    _correlation_id_var.set(correlation_id)


def _add_correlation_id(logger: structlog.BoundLogger, method_name: str, event_dict: dict) -> dict:
    correlation_id = get_correlation_id()
    if correlation_id:
        event_dict["correlation_id"] = correlation_id
    return event_dict


class _LoggingConfig:
    _configured = False

    @classmethod
    def is_configured(cls) -> bool:
        return cls._configured

    @classmethod
    def mark_configured(cls) -> None:
        cls._configured = True


def _setup() -> None:
    if _LoggingConfig.is_configured():
        return

    settings = get_settings()

    processors = [
        _add_correlation_id,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if settings.log_format_json:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

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
    def __init__(self, logger: structlog.BoundLogger) -> None:
        self._logger = logger

    def debug(self, message: str, **kwargs: object) -> None:
        self._logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs: object) -> None:
        self._logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs: object) -> None:
        self._logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs: object) -> None:
        exc_info = kwargs.pop("exc_info", True)
        self._logger.error(message, **kwargs, exc_info=exc_info)


def get_logger(name: str) -> SimpleLogger:
    _setup()

    logger = structlog.get_logger(name)
    return SimpleLogger(logger)
