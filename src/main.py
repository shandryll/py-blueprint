from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.exceptions.application_errors import ApplicationServiceError
from src.core.exceptions.fastapi_handlers import (
    application_error_handler,
    http_exception_handler,
    validation_exception_handler,
)
from src.core.middleware import HttpLoggingMiddleware
from src.core.settings import get_settings
from src.routes.health import router as health_router
from src.routes.products import router as products_router
from src.utils.logger import get_logger

# Carrega configurações
settings = get_settings()

# Application logging (auto-configured on first call)
logger = get_logger(__name__)

# Cria a aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
)

# Registra middleware (ordem inversa: último adicionado executa primeiro)
# Logging HTTP deve ser o primeiro executado
app.add_middleware(HttpLoggingMiddleware)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Registra exception handlers
app.add_exception_handler(ApplicationServiceError, application_error_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Inclui rotas
app.include_router(health_router)
app.include_router(products_router)
