from fastapi import APIRouter

from src.routes.products import delete, get, patch, post, put

router = APIRouter(prefix="/api/products", tags=["products"])

router.include_router(get.router)
router.include_router(post.router)
router.include_router(put.router)
router.include_router(patch.router)
router.include_router(delete.router)

__all__ = ["router"]
