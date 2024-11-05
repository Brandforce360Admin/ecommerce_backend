import datetime
import enum
import uuid

from sqlalchemy import Column, Enum, UUID, TIMESTAMP, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.base import Base


class OrderStatus(enum.Enum):
    pending = "Pending"
    confirmed = "Confirmed"
    preparing = "Preparing"
    completed = "Completed"
    cancelled = "Cancelled"


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    total_amount = Column(Float, nullable=False, default=0.0)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.pending)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC),
                         onupdate=datetime.datetime.now(datetime.UTC), nullable=True)
    users = relationship("User", back_populates="_orders")
    order_items = relationship("OrderItem", back_populates="_order")