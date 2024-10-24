import re
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.logger import logger


class LoginUserBase(BaseModel):
    email: EmailStr = Field(..., description="A valid email address.")


class LoginUserRequest(LoginUserBase):
    password: str = Field(..., min_length=8,
                          description="Password must be at least 8 characters long. Should contain ine uppercase, one numeral and one special character")

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"INFO: Login initiated for user with: {self.email}.\n")

    @field_validator("password")
    def validate_password(cls, password):
        """
        Custom password validator that checks for:
        - At least one uppercase letter
        - At least one numberlass
        - At least one special character
        """
        try:
            if not re.search(r"[A-Z]", password):
                raise ValueError("ERROR: Password must contain at least one uppercase letter.\n")
            if not re.search(r"\d", password):  # Checks for digits
                raise ValueError("ERROR: Password must contain at least one number.\n")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Checks for special characters
                raise ValueError("ERROR: Password must contain at least one special character.\n")
            return password
        except ValueError as e:
            logger.error(str(e))
            raise HTTPException(status_code=400, detail=str(e))


class LoginUserDetailsSchema(BaseModel):
    user_id: UUID
    name: str
    email: str


class LoginUserTokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class LoginUserResponse(BaseModel):
    user_details: LoginUserDetailsSchema
    tokens: LoginUserTokenSchema

    class Config:
        from_attributes = True
