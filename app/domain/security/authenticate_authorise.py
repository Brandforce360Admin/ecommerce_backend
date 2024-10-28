from uuid import UUID

from fastapi import Depends

from app.domain.security.session_validator import SessionValidator
from app.domain.value_objects.session_id import SessionId


class AuthenticationAndAuthorisation:
    def __init__(self, required_role: str):
        self.required_role = required_role

    def __call__(self, user_id: UUID,
                                   session_id: SessionId = Depends(SessionValidator)):
        return session_id
