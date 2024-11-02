import uuid

from sqlalchemy import Column, UUID, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.domain.models.cart_items_extras import cart_item_extras_table


class CartItem(Base):
    __tablename__ = "cart_items"

    _cart_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    _cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.cart_id"), nullable=False)
    _product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"), nullable=False)
    _quantity = Column(Integer, nullable=False,default=1)
    _cart = relationship("Cart", back_populates="_cart_items")
    _product = relationship("Product")
    _extras = relationship("Extra", secondary=cart_item_extras_table, back_populates="_cart_items")
