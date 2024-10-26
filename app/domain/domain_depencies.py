import datetime
import uuid

import jwt
from fastapi import Depends
from jwt import InvalidTokenError

from app.core.config import settings
from app.domain.excptions.authentication_exceptions import TokenExpiredException, InvalidTokenException, \
    UserAccessException
from app.domain.models.users import UserRole
from app.domain.value_objects.session_id import SessionId
from app.domain.value_objects.tokens import AccessToken
from app.domain.value_objects.user_id import UserId


def authenticate_user_access(required_role: UserRole, access_token: AccessToken):
    secret_key = settings.JWT_SECRET
    try:
        payload = jwt.decode(access_token.access_token, secret_key, algorithms=[settings.ALGORITHM])
        expiry: datetime = payload.get("exp")
        if expiry < datetime.datetime.now(datetime.UTC):
            raise TokenExpiredException("Access token expired")
        iat: datetime = payload.get("iat")
        access_token_expiration = iat + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)
        if access_token_expiration != expiry:
            raise InvalidTokenException("Access token is invalid")
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise InvalidTokenException("Access token does not contain user_id")
        role: str = payload.get("role")
        if role is None:
            raise InvalidTokenException("Access token does not contain role")
        if role != required_role.value:
            raise UserAccessException("User is not authorised to access the resource")
        session_id: str = payload.get("session_id")
        if session_id is None:
            raise InvalidTokenException("Access token does not contain session_id")
        return UserId(user_id=uuid.UUID(user_id)), SessionId(session_id=uuid.UUID(session_id))
    except InvalidTokenError:
        raise InvalidTokenException("Error decoding access_token")


def authenticate_user(user_id: UserId, session_id:SessionId = Depends(authenticate_user_access)):
    pass
