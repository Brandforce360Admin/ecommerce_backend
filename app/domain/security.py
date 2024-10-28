import datetime
from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from app.core.config import settings
from app.dependencies import get_session_repository
from app.domain.excptions.authentication_exceptions import TokenExpiredException, InvalidTokenException, \
    UserNonLoggedInException, UserAccessException
from app.domain.repositories.session_repository import SessionRepository
from app.domain.value_objects.session_id import SessionId
from app.domain.value_objects.user_id import UserId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenValidator:
    def __init__(self, required_role: str):
        self.required_role = required_role

    def __call__(self, user_id: UUID, access_token: str = Depends(oauth2_scheme)):
        secret_key = settings.JWT_SECRET
        try:
            payload = jwt.decode(access_token, secret_key, algorithms=[settings.ALGORITHM])
            expiry = datetime.datetime.fromtimestamp(payload.get("exp"), datetime.UTC)
            if expiry < datetime.datetime.now(datetime.UTC):
                raise TokenExpiredException("Access token expired")
            iat = datetime.datetime.fromtimestamp(payload.get("iat"), datetime.UTC)
            access_token_expiration = iat + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)
            if access_token_expiration != expiry:
                raise InvalidTokenException("Access token is invalid")
            decoded_user_id: str = payload.get("user_id")
            if decoded_user_id is None:
                raise InvalidTokenException("Access token does not contain user_id")
            if UUID(decoded_user_id) != user_id:
                raise InvalidTokenException("Access token is invalid")
            role: str = payload.get("role")
            if role is None:
                raise InvalidTokenException("Access token does not contain role")
            if role != self.required_role:
                raise UserAccessException("User is not authorised to access the resource")
            session_id: str = payload.get("session_id")
            if session_id is None:
                raise InvalidTokenException("Access token does not contain session_id")
            return SessionId(session_id=UUID(session_id))
        except InvalidTokenError:
            raise InvalidTokenException("Error decoding access_token")

def decode_and_validate_token(user_id: UUID, required_role: str, access_token: str = Depends(oauth2_scheme)):
    secret_key = settings.JWT_SECRET
    try:
        payload = jwt.decode(access_token, secret_key, algorithms=[settings.ALGORITHM])
        expiry = datetime.datetime.fromtimestamp(payload.get("exp"), datetime.UTC)
        if expiry < datetime.datetime.now(datetime.UTC):
            raise TokenExpiredException("Access token expired")
        iat = datetime.datetime.fromtimestamp(payload.get("iat"), datetime.UTC)
        access_token_expiration = iat + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)
        if access_token_expiration != expiry:
            raise InvalidTokenException("Access token is invalid")
        decoded_user_id: str = payload.get("user_id")
        if decoded_user_id is None:
            raise InvalidTokenException("Access token does not contain user_id")
        if UUID(decoded_user_id) != user_id:
            raise InvalidTokenException("Access token is invalid")
        role: str = payload.get("role")
        if role is None:
            raise InvalidTokenException("Access token does not contain role")
        if role != required_role:
            raise UserAccessException("User is not authorised to access the resource")
        session_id: str = payload.get("session_id")
        if session_id is None:
            raise InvalidTokenException("Access token does not contain session_id")
        return SessionId(session_id=UUID(session_id))
    except InvalidTokenError:
        raise InvalidTokenException("Error decoding access_token")


def validate_user_session_from_token(user_id: UUID, required_role: str,
                                     session_id: SessionId = Depends(decode_and_validate_token),
                                     session_repository: SessionRepository = Depends(get_session_repository)):
    user_session = session_repository.get_session_by_ids(user_id=UserId(user_id),
                                                         session_id=session_id)

    if user_session is None:
        raise UserNonLoggedInException(f"User with user_id {user_id} is not logged in")
    return session_id
