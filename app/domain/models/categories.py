import datetime
import uuid

from sqlalchemy import Column, UUID, String, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db.base import Base


class Category(Base):
    _tablename__ = "categories"

    category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC),
                        onupdate=datetime.datetime.now(datetime.UTC), nullable=True)
    products = relationship("Product", back_populates="_category")
