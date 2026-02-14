from fastapi import APIRouter

from src.routes.health import get

router = APIRouter(prefix="/api/v1/health", tags=["health"])

router.include_router(get.router)

__all__ = ["router"]
