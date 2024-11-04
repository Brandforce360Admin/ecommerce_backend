from app.domain.models.carts import Cart
from app.domain.models.users import User


class CartService:
    def __init__(self, cart_repository):
        self.cart_repository = cart_repository

    def check_and_create_user_cart(self, user: User) -> Cart:
        user_cart = self.cart_repository.get_user_cart(user)
        if user_cart:
            return user_cart
        else:
            return self.cart_repository.create_user_cart(user)


