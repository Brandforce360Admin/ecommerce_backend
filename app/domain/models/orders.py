import uuid

from sqlalchemy import Column, String, Enum, UUID, TIMESTAMP, ForeignKey
from db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    total_price = Column(String(100), nullable=False)
    status = Column(Enum("pending", "shipped", "delivered", "cancelled", name="order_status"), nullable=False,
                    default="pending")
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=True)
