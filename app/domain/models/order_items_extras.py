from sqlalchemy import (
    Column, ForeignKey, Table, UUID
)

from app.db.base import Base

order_item_extras_table = Table(
    'order_item_extras', Base.metadata,
    Column('_order_item_id', UUID, ForeignKey('order_items._order_item_id'), primary_key=True),
    Column('_extra_id', UUID, ForeignKey('extras._extra_id'), primary_key=True)
)