from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CartItemBase(BaseModel):
    product_id: UUID
    quantity: int


class CartItemCreate(CartItemBase):
    cart_id: UUID


class CartItemResponse(CartItemBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
