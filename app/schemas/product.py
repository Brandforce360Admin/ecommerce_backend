from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    stock: int


class ProductCreate(ProductBase):
    category_id: UUID


class ProductResponse(ProductBase):
    id: UUID
    category_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
