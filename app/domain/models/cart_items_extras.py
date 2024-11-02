from sqlalchemy import (
    Column, ForeignKey, Table, UUID
)

from app.db.base import Base

cart_item_extras_table = Table(
    'cart_item_extras', Base.metadata,
    Column('cart_item_id', UUID, ForeignKey('cart_items.id'), primary_key=True),
    Column('extra_id', UUID, ForeignKey('extras.id'), primary_key=True)
)