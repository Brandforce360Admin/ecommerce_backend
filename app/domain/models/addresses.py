import datetime
import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey, UUID, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db.base import Base


class Address(Base):
    __tablename__ = "addresses"

    _address_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    _user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    _label = Column(String(20), nullable=False)
    _address_line1 = Column(String(255), nullable=False)
    _address_line2 = Column(String(255), nullable=True)
    _address_line3 = Column(String(255), nullable=True)
    _city = Column(String(100), nullable=False)
    _state = Column(String(100), nullable=False)
    _postal_code = Column(String(20), nullable=False)
    _country = Column(String(100), nullable=False)
    _is_billing = Column(Boolean, default=False)
    _is_shipping = Column(Boolean, default=False)
    _created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC), nullable=False)
    _updated_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC),
                         onupdate=datetime.datetime.now(datetime.UTC), nullable=True)
    _user = relationship("User", back_populates="_addresses")
