from app.domain.value_objects.ids.product_id import ProductId
from app.domain.value_objects.ids.user_id import UserId
from app.domain.value_objects.quantity import Quantity


class CartApplication:
    def __init__(self):
        pass

    def add_product_to_user_cart(self, user_id: UserId, product_id: ProductId, quantity: Quantity):
        # Verify if cart exists
        # Verify if product in cart exists
        # If product exists update  quantity else update original request
        pass

    def get_user_cart(self, user_id: UserId):
        # Return full cart with product and extras
        pass

    def empty_user_cart(self, user_id: UserId):
        pass

    def remove_product_from_user_cart(self, user_id: UserId, product_id: ProductId):
        pass

    def update_product_for_user_cart(self, user_id: UserId, product_id: ProductId, quantity: Quantity):
        pass
