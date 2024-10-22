from pydantic import BaseModel, EmailStr, Field


class LogoutUserResponse(BaseModel):
    email: EmailStr = Field(..., description="A valid email address.")
