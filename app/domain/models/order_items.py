import uuid

from sqlalchemy import Column, UUID, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.domain.models.order_items_extras import order_item_extras_table


class OrderItem(Base):
    _tablename__ = "order_items"

    order_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders._order_id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products._product_id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)
    order = relationship("Order", back_populates="_order_items")
    product = relationship("Product")
    extras = relationship("Extra", secondary=order_item_extras_table, back_populates="_order_items")
