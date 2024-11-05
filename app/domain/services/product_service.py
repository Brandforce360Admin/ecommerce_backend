from app.domain.excptions.product_exceptions import ProductDoesNotExistsException, ProductNotAvailableException
from app.domain.models.products import Product


class ProductService:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def check_existence_and_return_product(self, product: Product) -> Product:
        db_product = self.product_repository.get_product(product)
        if db_product is None:
            raise ProductDoesNotExistsException(f"Product with product id {product.product_id} does not exists")
        else:
            if db_product.is_available:
                return db_product
            else:
                raise ProductNotAvailableException(f"Product with product id {product.product_id} is not available")
