import uuid


class CartId:
    def __init__(self, cart_id: uuid.UUID):
        self._cart_id = cart_id

    @property
    def cart_id(self):
        return self._cart_id

    @cart_id.setter
    def cart_id(self, cart_id):
        self._cart_id = cart_id
