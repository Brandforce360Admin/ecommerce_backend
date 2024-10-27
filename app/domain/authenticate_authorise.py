import datetime
from typing import Tuple
from uuid import UUID

import jwt
from fastapi import Depends
from fastapi import Path
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from app.core.config import settings
from app.dependencies import get_session_repository
from app.domain.excptions.authentication_exceptions import TokenExpiredException, InvalidTokenException, \
    UserAccessException, UserNonLoggedInException
from app.domain.models.users import UserRole
from app.domain.repositories.session_repository import SessionRepository
from app.domain.value_objects.session_id import SessionId
from app.domain.value_objects.user_id import UserId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_and_authorise_user(required_role: str, user_id: UUID = Path(...)):
    def dependency(access_token: str = Depends(oauth2_scheme)) -> Tuple[UserId, SessionId]:
        secret_key = settings.JWT_SECRET
        try:
            payload = jwt.decode(access_token, secret_key, algorithms=[settings.ALGORITHM])

            expiry: datetime = payload.get("exp")
            if expiry < datetime.datetime.now(datetime.UTC):
                raise TokenExpiredException("Access token expired")
            iat: datetime = payload.get("iat")
            access_token_expiration = iat + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)
            if access_token_expiration != expiry:
                raise InvalidTokenException("Access token is invalid")
            decoded_user_id: str = payload.get("user_id")
            if decoded_user_id is None:
                raise InvalidTokenException("Access token does not contain user_id")
            if decoded_user_id != user_id:
                raise InvalidTokenException("Access token is invalid")
            role: str = payload.get("role")
            if role is None:
                raise InvalidTokenException("Access token does not contain role")
            if role != required_role:
                raise UserAccessException("User is not authorised to access the resource")
            session_id: str = payload.get("session_id")
            if session_id is None:
                raise InvalidTokenException("Access token does not contain session_id")
            new_user_id = UserId(user_id=user_id)
            user_session_id = SessionId(session_id=UUID(session_id))
            validate_user_session(user_id=new_user_id, session_id=user_session_id)
        except InvalidTokenError:
            raise InvalidTokenException("Error decoding access_token")
        return new_user_id, user_session_id

    return dependency


def validate_user_session(user_id: UserId, session_id: SessionId,
                          session_repository: SessionRepository = Depends(get_session_repository)):
    user_session = session_repository.get_session_by_ids(user_id=user_id,
                                                         session_id=session_id)
    if user_session is None:
        raise UserNonLoggedInException(f"User with user_id {user_id.user_id} is not logged in")
