from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class ProductExtras(BaseModel):
    extra_id: UUID = Field(..., description="Id of the associated Product Extra")
    extra_name: str = Field(..., description="Name of the associated Product Extra")
    quantity: int = Field(..., description="Quantity of the extra")
    extra_img_url: str = Field(..., description="Image url of the extra")


class AddProductExtras(BaseModel):
    extra_id: UUID = Field(..., description="Id of the associated Product Extra")
    quantity: int = Field(..., description="Quantity of the extra")


class AddProductToCartRequest(BaseModel):
    product_id: UUID = Field(..., description="Product ID of the Product")
    quantity: int = Field(..., description="Quantity of the Product")
    extras: List[AddProductExtras]


class UpdateProductOfCartRequest(BaseModel):
    product_id: UUID = Field(..., description="Product ID of the Product")
    quantity: int = Field(..., description="Quantity of the Product")
    extras: List[AddProductExtras]


class GetUserCart(BaseModel):
    product_id: UUID = Field(..., description="Product ID of the Product")
    product_name: str = Field(..., description="Name of the Product")
    product_img_url: str = Field(..., description="Image url of the Product")
    quantity: int = Field(..., description="Quantity of the Product")
    extras: List[ProductExtras]


class GetUserCartResponse(BaseModel):
    cart_details: List[GetUserCart]
