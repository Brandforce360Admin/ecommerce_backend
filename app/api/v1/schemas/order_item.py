from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class OrderItemBase(BaseModel):
    product_id: UUID
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    order_id: UUID


class OrderItemResponse(OrderItemBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
