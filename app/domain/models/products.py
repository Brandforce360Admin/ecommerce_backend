import datetime
import uuid

from sqlalchemy import Column, UUID, String, TIMESTAMP, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.domain.models.product_extras import product_extras_table


class Product(Base):
    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.category_id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    is_available = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC),
                        onupdate=datetime.datetime.now(datetime.UTC), nullable=True)
    category = relationship("Category", back_populates="products")
    extras = relationship("Extra", secondary=product_extras_table, back_populates="products")

    def __init__(self, product_id: UUID):
        self._product_id = product_id
