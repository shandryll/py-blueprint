from fastapi import APIRouter

from src.routes.health import get

router = APIRouter(prefix="/health", tags=["health"])

router.include_router(get.router)

__all__ = ["router"]
