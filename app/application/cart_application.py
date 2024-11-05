from typing import Dict

from app.domain.models.carts import Cart
from app.domain.models.extras import Extra
from app.domain.models.products import Product
from app.domain.models.users import User
from app.domain.value_objects.ids.product_id import ProductId
from app.domain.value_objects.ids.user_id import UserId
from app.domain.value_objects.quantity import Quantity


class CartApplication:
    def __init__(self, cart_service, product_service, extras_service):
        self.cart_service = cart_service
        self.product_service = product_service
        self.extras_service = extras_service

    def add_product_to_user_cart(self, user: User, product: Product, product_quantity: Quantity,
                                 extras_and_quantity: Dict[Extra, Quantity]) -> Cart:
        product = self.product_service.check_existence_and_return_product(product)
        extras_and_quantity = self.extras_service.check_extras_for_product(extras_and_quantity, product)
        user_cart = self.cart_service.check_and_create_user_cart(user)
        cart_item = self.cart_service.create_cart_item(user_cart, product, product_quantity, extras_and_quantity)
        user_cart = self.cart_service.add_cart_item_to_user_cart(user_cart, cart_item)
        return user_cart

    def get_user_cart(self, user: User):
        # Return full cart with product and extras
        pass

    def empty_user_cart(self, user_id: UserId):
        pass

    def remove_product_from_user_cart(self, user_id: UserId, product_id: ProductId):
        pass

    def update_product_for_user_cart(self, user_id: UserId, product_id: ProductId, quantity: Quantity):
        pass
