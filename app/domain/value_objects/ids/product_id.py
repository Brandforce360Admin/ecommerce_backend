import uuid


class ProductId:
    def __init__(self, product_id: uuid.UUID):
        self._product_id = product_id

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        self._product_id = product_id
