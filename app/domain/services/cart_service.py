from typing import Dict

from app.domain.models.cart_items import CartItem
from app.domain.models.carts import Cart
from app.domain.models.extras import Extra
from app.domain.models.products import Product
from app.domain.models.users import User
from app.domain.value_objects.quantity import Quantity


class CartService:
    def __init__(self, cart_repository):
        self.cart_repository = cart_repository

    def check_and_create_user_cart(self, user: User) -> Cart:
        user_cart = self.cart_repository.get_user_cart(user)
        if user_cart:
            return user_cart
        else:
            return self.cart_repository.create_user_cart(user)

    def create_cart_item(self, cart: Cart, product: Product, product_quantity: Quantity,
                         extras: Dict[Extra, Quantity]) -> CartItem:
        pass

    def add_cart_item_to_user_cart(self, user_cart: Cart, cart_item: CartItem):
        pass
