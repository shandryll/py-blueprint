from fastapi import APIRouter, status

from src.controllers import HealthController

router = APIRouter()

_health_controller = HealthController()


@router.get("/", status_code=status.HTTP_200_OK)
async def health() -> dict[str, str]:
    """Endpoint de saúde da aplicação.

    Verifica se a aplicação está funcionando corretamente.

    Returns:
        dict[str, str]: Status da aplicação com versão e timestamp.
    """
    return await _health_controller.check()