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
