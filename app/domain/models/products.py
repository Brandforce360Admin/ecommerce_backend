import uuid

from sqlalchemy import Column, UUID, String, TIMESTAMP, ForeignKey, Integer
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(String(100), nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=True)
