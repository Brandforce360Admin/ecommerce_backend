from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CartBase(BaseModel):
    user_id: UUID

class CartCreate(CartBase):
    pass

class CartResponse(CartBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
