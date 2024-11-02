import datetime
import uuid

from sqlalchemy import Column, String, Float, UUID, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.domain.models.order_items_extras import order_item_extras_table
from app.domain.models.product_extras import product_extras_table


class Extra(Base):
    __tablename__ = 'extras'

    _extra_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    _name = Column(String, nullable=False)
    _description = Column(String, nullable=True)
    _price = Column(Float, nullable=False)
    _created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC), nullable=False)
    _updated_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC),
                         onupdate=datetime.datetime.now(datetime.UTC), nullable=True)

    _products = relationship("Product", secondary=product_extras_table, back_populates="_extras")
    _order_items = relationship("OrderItem", secondary=order_item_extras_table, back_populates="_extras")
