from src.main import app


def test_app_creation() -> None:
    """Testa se a app FastAPI foi criada."""
    assert app.title == "Py-Blueprint"
