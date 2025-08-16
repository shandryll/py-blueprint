from src.calculadora import soma


def test_soma():
    """Checks if the sum of two numbers is correct."""
    assert soma(2, 3) == 5
    assert soma(-1, 1) == 0
    assert soma(0, 0) == 0
