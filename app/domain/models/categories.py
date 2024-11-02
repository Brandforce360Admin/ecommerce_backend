import datetime
import uuid

from sqlalchemy import Column, UUID, String, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    _category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    _name = Column(String(100), nullable=False)
    _description = Column(String(255), nullable=True)
    _created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC), nullable=False)
    _updated_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC),
                        onupdate=datetime.datetime.now(datetime.UTC), nullable=True)
    _products = relationship("Product", back_populates="_category")
