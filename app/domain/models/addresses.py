import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey, UUID, TIMESTAMP

from app.db.base import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    is_billing = Column(Boolean, default=False)
    is_shipping = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, nullable=False)
