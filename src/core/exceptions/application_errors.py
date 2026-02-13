from functools import lru_cache

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
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8080"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    cors_allow_headers: list[str] = ["Content-Type", "Authorization", "Accept"]

    # Logging
    log_level: str = "INFO"
    log_format_json: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Retorna as configurações da aplicação.

    Usa cache para garantir que apenas uma instância seja criada (singleton pattern).

    Returns:
        Settings: Instância das configurações (cached).
    """
    return Settings()
