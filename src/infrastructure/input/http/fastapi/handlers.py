from datetime import UTC, datetime
from typing import cast

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.domain.exceptions.product_exceptions import (
    ProductDomainError,
    ProductNotFoundError,
    ProductValidationError,
)
from src.shared.exceptions import ApplicationServiceError


async def application_error_handler(request: Request, exc: Exception) -> JSONResponse:
    app_error = cast(ApplicationServiceError, exc)
    error_dict = app_error.to_dict()
    error_dict.update(
        {
            "timestamp": datetime.now(UTC).isoformat(),
            "path": str(request.url.path),
        }
    )

    return JSONResponse(
        status_code=app_error.status_code,
        content=error_dict,
    )


async def product_domain_error_handler(request: Request, exc: ProductDomainError) -> JSONResponse:
    if isinstance(exc, ProductNotFoundError):
        status_code = 404
    elif isinstance(exc, ProductValidationError):
        status_code = 422
    else:
        status_code = 409

    error_dict = {
        "error": "Domain Error",
        "message": exc.message,
        "error_code": exc.code,
        "status_code": status_code,
        "timestamp": datetime.now(UTC).isoformat(),
        "path": str(request.url.path),
    }

    return JSONResponse(
        status_code=status_code,
        content=error_dict,
    )


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    http_exc = cast(StarletteHTTPException, exc)
    error_dict = {
        "error": "HTTP Exception",
        "message": http_exc.detail,
        "error_code": "NOT_FOUND" if http_exc.status_code == 404 else "HTTP_ERROR",
        "status_code": http_exc.status_code,
        "timestamp": datetime.now(UTC).isoformat(),
        "path": str(request.url.path),
    }

    return JSONResponse(
        status_code=http_exc.status_code,
        content=error_dict,
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    validation_exc = cast(RequestValidationError, exc)
    errors = [
        {
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        }
        for error in validation_exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Validation error in the provided data",
            "error_code": "VALIDATION_ERROR",
            "status_code": 422,
            "errors": errors,
            "timestamp": datetime.now(UTC).isoformat(),
            "path": str(request.url.path),
        },
    )
