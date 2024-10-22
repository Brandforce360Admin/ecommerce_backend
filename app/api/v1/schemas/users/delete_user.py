from pydantic import BaseModel, EmailStr, Field


class DeleteUserResponse(BaseModel):
    email: EmailStr = Field(..., description="A valid email address.")
