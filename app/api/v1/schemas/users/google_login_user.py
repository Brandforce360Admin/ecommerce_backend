from pydantic import BaseModel, Field

from app.logger import logger


class GoogleLoginRequest(BaseModel):
    token: str = Field(..., description="Token from client")

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"INFO: Login initiated for Google User.\n")
