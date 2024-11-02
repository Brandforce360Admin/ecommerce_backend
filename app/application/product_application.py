from app.domain.models.products import Product
from app.domain.value_objects.ids.product_id import ProductId


class ProductApplication:
    def __init__(self):
        pass

    def add_new_product(self, product: Product):
        pass

    def get_all_product_list(self):
        pass

    def get_product_item_details(self, product_id: ProductId):
        pass

    def update_product_item_details(self, product_id: ProductId):
        pass

    def delete_product_item_details(self, product_id: ProductId):
        pass
