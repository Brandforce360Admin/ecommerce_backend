import datetime
import uuid

from sqlalchemy import Column, String, Float, UUID, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.domain.models.order_items_extras import order_item_extras_table
from app.domain.models.product_extras import product_extras_table


class Extra(Base):
    __tablename__ = 'extras'

    extra_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC),
                         onupdate=datetime.datetime.now(datetime.UTC), nullable=True)

    products = relationship("Product", secondary=product_extras_table, back_populates="extras")
    order_items = relationship("OrderItem", secondary=order_item_extras_table, back_populates="extras")
