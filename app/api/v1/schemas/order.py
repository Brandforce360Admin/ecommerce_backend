from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: UUID
    total_price: float
    status: str


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
