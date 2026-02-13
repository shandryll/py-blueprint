from src.models.product import ProductResponse


def format_product_response(product: ProductResponse) -> dict:
    """Formata a resposta de um produto para apresentação.

    Args:
        product: Produto a ser formatado.

    Returns:
        dict: Dicionário com dados formatados do produto.
    """
    stock_status = "esgotado" if product.stock == 0 else ("estoque_baixo" if product.stock < 5 else "disponível")

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "price_formatted": f"R$ {product.price:,.2f}".replace(",", "."),
        "stock": product.stock,
        "stock_status": stock_status,
        "created_at": product.created_at.isoformat() if product.created_at else None,
        "updated_at": product.updated_at.isoformat() if product.updated_at else None,
    }


def format_products_list_response(products: list[ProductResponse]) -> list[dict]:
    """Formata uma lista de produtos para apresentação.

    Args:
        products: Lista de produtos a serem formatados.

    Returns:
        list[dict]: Lista de dicionários com dados formatados dos produtos.
    """
    return [format_product_response(product) for product in products]


def format_product_summary(product: ProductResponse) -> dict:
    """Formata um resumo simplificado de um produto.

    Args:
        product: Produto a ser resumido.

    Returns:
        dict: Dicionário com resumo do produto.
    """
    stock_status = "esgotado" if product.stock == 0 else ("estoque_baixo" if product.stock < 5 else "disponível")

    return {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "price_formatted": f"R$ {product.price:,.2f}".replace(",", "."),
        "stock": product.stock,
        "stock_status": stock_status,
    }
