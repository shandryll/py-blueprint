from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.domain.exceptions.product_exceptions import ProductDomainError
from src.infrastructure.di.container import build_product_use_case
from src.infrastructure.input.http.fastapi.handlers import (
    application_error_handler,
    http_exception_handler,
    product_domain_error_handler,
    validation_exception_handler,
)
from src.infrastructure.input.http.fastapi.middleware import HttpLoggingMiddleware
from src.infrastructure.input.http.fastapi.routes import health, products
from src.infrastructure.output.persistence.in_memory.product_repository import InMemoryProductRepository
from src.shared.exceptions import ApplicationServiceError
from src.shared.logger import get_logger
from src.shared.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger = get_logger(__name__)
    logger.info("Application started")
    yield
    logger.info("Application shutting down")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(lifespan=lifespan)

    repo = InMemoryProductRepository()
    app.state.product_use_case = build_product_use_case(repo)

    app.add_middleware(HttpLoggingMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    app.add_exception_handler(ApplicationServiceError, application_error_handler)
    app.add_exception_handler(ProductDomainError, product_domain_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    app.include_router(health.router)
    app.include_router(products.router)

    return app
