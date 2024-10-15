import uuid

from sqlalchemy import Column, UUID, String, TIMESTAMP, ForeignKey
from app.db.base import Base



class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
