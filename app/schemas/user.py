import re
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="The user's full name.")
    email: EmailStr = Field(..., description="A valid email address.")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8,
                          description="Password must be at least 8 characters long. Should contain ine uppercase, one numeral and one special character")

    @field_validator("password")
    def validate_password(cls, password):
        """
        Custom password validator that checks for:
        - At least one uppercase letter
        - At least one number
        - At least one special character
        """
        try:
            if not re.search(r"[A-Z]", password):
                raise ValueError("Password must contain at least one uppercase letter.")
            if not re.search(r"\d", password):  # Checks for digits
                raise ValueError("Password must contain at least one number.")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Checks for special characters
                raise ValueError("Password must contain at least one special character.")
            return password
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


class UserResponse(UserBase):
    user_id: UUID
    created_at: datetime

    def __init__(self, user_id: UUID, name: str, email: str, created_at: datetime):
        super().__init__(name=name, email=email)
        self.user_id = user_id
        self.created_at = created_at

    class Config:
        from_attributes = True
