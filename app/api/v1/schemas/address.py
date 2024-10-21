from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AddressBase(BaseModel):
    address_line1: str
    address_line2: Optional[str]
    address_line3: Optional[str]
    city: str
    state: str
    postal_code: str
    country: str
    is_billing: bool = False
    is_shipping: bool = False


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True
