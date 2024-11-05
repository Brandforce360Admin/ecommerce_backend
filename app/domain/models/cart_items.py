import uuid

from sqlalchemy import Column, UUID, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.domain.models.cart_items_extras import cart_item_extras_table


class CartItem(Base):
    __tablename__ = "cart_items"

    cart_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.cart_id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False,default=1)
    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product")
    extras = relationship("Extra", secondary=cart_item_extras_table, back_populates="cart_items")
