"""Middleware da aplicação."""

from src.core.middleware.http_logging import HttpLoggingMiddleware

__all__ = ["HttpLoggingMiddleware"]
