from datetime import UTC, datetime

from fastapi import APIRouter

from src.core.config import get_settings

router = APIRouter()


@router.get("/health", status_code=200)
async def health() -> dict[str, str]:
    """Endpoint de saúde da aplicação.

    Verifica se a aplicação está funcionando corretamente.

    Returns:
        dict[str, str]: Status da aplicação com versão e timestamp.
    """
    settings = get_settings()

    return {
        "status": "healthy",
        "version": settings.app_version,
        "timestamp": datetime.now(UTC).isoformat(),
    }
