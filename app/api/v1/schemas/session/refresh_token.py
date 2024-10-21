from uuid import UUID

from pydantic import BaseModel, Field


class RefreshTokenRequest(BaseModel):
    user_id: UUID = Field(..., description="User Id for the user")


class RefreshTokenResponse(BaseModel):
    access_token: str = Field(..., description="Access Token for the user")
