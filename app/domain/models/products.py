import datetime
import uuid

from sqlalchemy import Column, UUID, String, TIMESTAMP, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.domain.models.product_extras import product_extras_table


class Product(Base):
    __tablename__ = "products"

    _product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    _category_id = Column(UUID(as_uuid=True), ForeignKey("categories.category_id"), nullable=False)
    _name = Column(String(100), nullable=False)
    _description = Column(String, nullable=True)
    _price = Column(Float, nullable=False)
    _image_url = Column(String, nullable=True)
    _created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC), nullable=False)
    _updated_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC),
                         onupdate=datetime.datetime.now(datetime.UTC), nullable=True)
    _category = relationship("Category", back_populates="_products")
    _extras = relationship("Extra", secondary=product_extras_table, back_populates="_products")

    def __init__(self, product_id: UUID):
        self._product_id = product_id

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        self._product_id = product_id

    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        self._category_id = category_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def image_url(self):
        return self._image_url

    @image_url.setter
    def image_url(self, image_url):
        self._image_url = image_url

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        self._created_at = created_at

    @property
    def updated_at(self):
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        self._updated_at = updated_at

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def extras(self):
        return self._extras

    @extras.setter
    def extras(self, extras):
        self._extras = extras
