from pytest import MonkeyPatch

from src.core.config import Settings


def test_settings_defaults() -> None:
    """Testa os valores padrão das configurações."""
    settings = Settings()
    assert settings.app_name == "Py-Blueprint"
    assert settings.app_version == "0.1.0"
    assert settings.app_description
    assert settings.port == 8000
    assert settings.cors_origins == ["*"]


def test_settings_env_override(monkeypatch: MonkeyPatch) -> None:
    """Testa que variáveis de ambiente sobrescrevem valores padrão."""
    monkeypatch.setenv("APP_NAME", "MyApp")
    monkeypatch.setenv("PORT", "9000")
    settings = Settings()
    assert settings.app_name == "MyApp"
    assert settings.port == 9000
