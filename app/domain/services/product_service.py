from typing import List

from app.domain.excptions.product_exceptions import ProductDoesNotExistsException
from app.domain.models.cart_items import CartItem
from app.domain.models.extras import Extra
from app.domain.models.products import Product


class CartService:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def check_if_product_exists(self, product: Product) -> Product:
        db_product = self.product_repository.get_product(product)
        if db_product is None:
            raise ProductDoesNotExistsException(f"Product with product id {product.product_id}")
        else:
            return db_product

    def create_cart_item(self, product: Product, extras: List[Extra] = None) -> CartItem:
        pass

    def add_cart_item_to_user_cart(self, cart_item: CartItem):
        pass
