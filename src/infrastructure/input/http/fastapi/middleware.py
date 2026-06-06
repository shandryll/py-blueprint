import time
import uuid
from collections.abc import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.shared.logger import get_logger, set_correlation_id

logger = get_logger(__name__)

CORRELATION_ID_HEADER = "X-Correlation-ID"


class HttpLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        correlation_id = request.headers.get(CORRELATION_ID_HEADER)
        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        set_correlation_id(correlation_id)

        method = request.method
        path = request.url.path
        client_host = request.client.host if request.client else "unknown"

        start_time = time.perf_counter()

        try:
            response = await call_next(request)

            process_time = time.perf_counter() - start_time

            response.headers[CORRELATION_ID_HEADER] = correlation_id

            logger.info(
                "http_request",
                correlation_id=correlation_id,
                method=method,
                path=path,
                status_code=response.status_code,
                duration_ms=round(process_time * 1000, 2),
                client_ip=client_host,
            )

            return response

        except Exception as exc:
            process_time = time.perf_counter() - start_time

            logger.error(
                "request_failed",
                correlation_id=correlation_id,
                method=method,
                path=path,
                error=str(exc),
                duration_ms=round(process_time * 1000, 2),
                client_ip=client_host,
                exc_info=True,
            )

            raise
