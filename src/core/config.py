"""Configurações da aplicação usando pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação.

    As configurações podem ser definidas via variáveis de ambiente ou arquivo .env.
    """

    # Aplicação
    app_name: str = "Py-Blueprint"
    app_version: str = "0.1.0"
    app_description: str = "Template MVC para Python"
    debug: bool = False

    # Servidor
    host: str = "0.0.0.0"  # nosec B104 - Valor padrão para desenvolvimento, pode ser sobrescrito via env
    port: int = 8000
    reload: bool = False

    # CORS
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


def get_settings() -> Settings:
    """Retorna as configurações da aplicação.

    Returns:
        Settings: Instância das configurações.
    """
    return Settings()
