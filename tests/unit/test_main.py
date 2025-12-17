"""Testes para o módulo main."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.main import app


def test_app_is_fastapi_instance() -> None:
    """Testa que app é uma instância do FastAPI."""
    assert isinstance(app, FastAPI)


def test_app_has_correct_title() -> None:
    """Testa que a app tem o título correto."""
    assert app.title == "Py-Blueprint"


def test_app_has_description() -> None:
    """Testa que a app tem descrição."""
    assert app.description == "Template MVC para Python"


def test_app_has_version() -> None:
    """Testa que a app tem versão."""
    assert app.version == "0.1.0"


def test_app_has_health_router() -> None:
    """Testa que a app inclui o router de health."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
