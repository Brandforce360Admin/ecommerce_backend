import uuid


class CategoryId:
    def __init__(self, category_id: uuid.UUID):
        self._category_id = category_id

    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        self._category_id = category_id
