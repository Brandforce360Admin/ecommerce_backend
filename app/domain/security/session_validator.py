from uuid import UUID

from fastapi import Depends

from app.dependencies import get_session_repository
from app.domain.excptions.authentication_exceptions import UserNonLoggedInException
from app.domain.repositories.session_repository import SessionRepository
from app.domain.security.token_validator import TokenValidator
from app.domain.value_objects.session_id import SessionId
from app.domain.value_objects.user_id import UserId


class SessionValidator:
    def __init__(self, required_role: str = None):
        self.required_role = required_role

    def __call__(self, user_id: UUID,
                 session_id: SessionId = Depends(TokenValidator),
                 session_repository: SessionRepository = Depends(get_session_repository)):
        user_session = session_repository.get_session_by_ids(user_id=UserId(user_id),
                                                             session_id=session_id)
        if user_session is None:
            raise UserNonLoggedInException(f"User with user_id {user_id} is not logged in")
        return session_id
