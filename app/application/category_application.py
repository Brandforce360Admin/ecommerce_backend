from app.domain.models.categories import Category
from app.domain.value_objects.ids.category_id import CategoryId


class CategoryApplication:
    def __init__(self):
        pass

    def add_new_category(self, category: Category):
        pass

    def list_all_categories(self):
        pass

    def list_products_in_category(self, category_id: CategoryId):
        pass

    def update_category(self, category_id: CategoryId):
        pass

    def delete_category(self, category_id: CategoryId):
        pass
