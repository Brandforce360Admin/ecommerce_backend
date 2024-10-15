import uuid

from sqlalchemy import Column, UUID, TIMESTAMP, ForeignKey
from db import Base


class Cart(Base):
    __tablename__ = "cart"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
