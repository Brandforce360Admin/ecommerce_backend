import uuid

from sqlalchemy import Column, UUID, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.domain.models.order_items_extras import order_item_extras_table


class OrderItem(Base):
    __tablename__ = "order_items"

    _order_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    _order_id = Column(UUID(as_uuid=True), ForeignKey("orders._order_id"), nullable=False)
    _product_id = Column(UUID(as_uuid=True), ForeignKey("products._product_id"), nullable=False)
    _quantity = Column(Integer, nullable=False, default=1)
    _price = Column(Float, nullable=False)
    _order = relationship("Order", back_populates="_order_items")
    _product = relationship("Product")
    _extras = relationship("Extra", secondary=order_item_extras_table, back_populates="_order_items")
