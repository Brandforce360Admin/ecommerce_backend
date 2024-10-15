import uuid

from sqlalchemy import Column, String, UUID, TIMESTAMP, ForeignKey, Integer
from db import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
