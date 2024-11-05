import datetime
import uuid

from sqlalchemy import Column, UUID, TIMESTAMP, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class Cart(Base):
    __tablename__ = "carts"

    cart_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    total_price = Column(Float, nullable=False, default=0.0)
    total_items = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC),
                        onupdate=datetime.datetime.now(datetime.UTC), nullable=True)

    user = relationship("User", back_populates="cart")
    cart_items = relationship("CartItem", back_populates="cart")
