from datetime import UTC, datetime

from src.core.settings import get_settings


class HealthController:
    """Controller para verificação de saúde da aplicação.

    Coordena a lógica de health check.
    """

    async def check(self) -> dict[str, str]:
        """Verifica a saúde da aplicação.

        Returns:
            dict[str, str]: Status da aplicação com versão e timestamp.
        """
        settings = get_settings()

        return {
            "status": "healthy",
            "version": settings.app_version,
            "timestamp": datetime.now(UTC).isoformat(),
        }
