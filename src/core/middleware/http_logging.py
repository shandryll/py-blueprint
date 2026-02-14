"""Middleware para logging estruturado de requisições HTTP."""

import time
import uuid
from collections.abc import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.utils.logger import get_logger, set_correlation_id

logger = get_logger(__name__)

# Nome do header para correlation ID
CORRELATION_ID_HEADER = "X-Correlation-ID"


class HttpLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware que loga todas as requisições HTTP com detalhes contextuais.

    Captura:
    - Método HTTP e caminho
    - Status code da resposta
    - Tempo de processamento
    - IP do cliente
    - User-Agent
    - Tamanho da resposta
    - Correlation ID para rastreamento distribuído
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Processa a requisição e a resposta, registrando o resultado final."""
        # Gera ou obtém Correlation ID (para rastreamento distribuído)
        correlation_id = request.headers.get(CORRELATION_ID_HEADER)
        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        # Armazena correlation ID no contexto para acesso em toda a request
        set_correlation_id(correlation_id)

        # Informações da requisição
        method = request.method
        path = request.url.path
        client_host = request.client.host if request.client else "unknown"

        # Tempo de início
        start_time = time.perf_counter()

        try:
            # Processa a requisição
            response = await call_next(request)

            # Tempo total de processamento
            process_time = time.perf_counter() - start_time

            # Adiciona correlation ID no header da resposta
            response.headers[CORRELATION_ID_HEADER] = correlation_id

            # Log de requisição processada
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
            # Tempo até o erro
            process_time = time.perf_counter() - start_time

            # Log de erro
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
