import uuid
import datetime
from sqlalchemy import Column, UUID, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Cart(Base):
    __tablename__ = "carts"

    cart_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC),
                         onupdate=datetime.datetime.now(datetime.UTC), nullable=True)

    user = relationship("User", back_populates="_cart")
    cart_items = relationship("CartItem", back_populates="_cart")
