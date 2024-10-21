from uuid import UUID

from pydantic import BaseModel, Field


class RefreshTokenRequest(BaseModel):
    user_id: UUID = Field(..., description="User Id for the user")
    refresh_token: str = Field(..., description="Refresh Token for User")
