from app.domain.excptions.product_exceptions import ProductDoesNotExistsException
from app.domain.models.products import Product


class CartService:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def check_if_product_exists(self, product: Product) -> Product:
        product = self.product_repository.get_product(product)
        if product is None:
            raise ProductDoesNotExistsException(f"Product with product id {product.product_id}")
        else:
            return product
