from sqlalchemy import (
    Column, ForeignKey, Table, UUID
)

from app.db.base import Base

product_extras_table = Table(
    'product_extras', Base.metadata,
    Column('_product_id', UUID, ForeignKey('products._product_id'), primary_key=True),
    Column('_extra_id', UUID, ForeignKey('extras._extra_id'), primary_key=True)
)
