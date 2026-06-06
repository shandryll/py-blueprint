from datetime import UTC, datetime

from fastapi import APIRouter

from src.infrastructure.input.http.fastapi.schemas.health_schemas import HealthResponseSchema
from src.shared.settings import get_settings

router = APIRouter(prefix="/api/v1/health", tags=["health"])


@router.get(
    "/",
    response_model=HealthResponseSchema,
    status_code=200,
)
async def health_check() -> HealthResponseSchema:
    settings = get_settings()
    return HealthResponseSchema(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.now(UTC).isoformat(),
    )
