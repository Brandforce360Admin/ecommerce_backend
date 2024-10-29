from uuid import UUID

from fastapi import Depends

from app.dependencies import get_session_repository
from app.domain.excptions.authentication_exceptions import UserAccessException, InvalidTokenException, \
    UserNonLoggedInException
from app.domain.repositories.session_repository import SessionRepository
from app.domain.security.decoded_token_details import DecodedTokenDetails
from app.domain.security.token_validator import TokenValidator
from app.domain.value_objects.session_id import SessionId


class AuthenticationAndAuthorisation:
    def __init__(self, required_role: str):
        self.required_role = required_role

    def __call__(self, user_id: UUID, decoded_token_details: DecodedTokenDetails = Depends(TokenValidator()),
                 session_repository: SessionRepository = Depends(get_session_repository)) -> SessionId:
        if decoded_token_details.role != self.required_role:
            raise UserAccessException("User is not authorised to access the resource")
        if decoded_token_details.user_id.user_id != user_id:
            raise InvalidTokenException("Invalid user id for the token")
        user_session = session_repository.get_session_by_ids(user_id=decoded_token_details.user_id,
                                                             session_id=decoded_token_details.session_id)
        if user_session is None:
            raise UserNonLoggedInException(f"User with user_id {user_id} is not logged in")
        return decoded_token_details.session_id
