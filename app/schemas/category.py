from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: Optional[str]


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: UUID
    parent_id: Optional[UUID]
    created_at: datetime

    class Config:
        orm_mode = True
