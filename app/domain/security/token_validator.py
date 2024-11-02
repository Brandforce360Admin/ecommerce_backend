import datetime
from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from app.core.config import settings
from app.domain.excptions.authentication_exceptions import TokenExpiredException, InvalidTokenException
from app.domain.security.decoded_token_details import DecodedTokenDetails
from app.domain.value_objects.ids.session_id import SessionId
from app.domain.value_objects.ids.user_id import UserId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenValidator:
    def __call__(self, access_token: str = Depends(oauth2_scheme)) -> DecodedTokenDetails:
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
            decoded_role: str = payload.get("role")
            if decoded_role is None:
                raise InvalidTokenException("Access token does not contain role")
            decoded_session_id: str = payload.get("session_id")
            if decoded_session_id is None:
                raise InvalidTokenException("Access token does not contain session_id")
            return DecodedTokenDetails(user_id=UserId(UUID(decoded_user_id)),
                                       session_id=SessionId(UUID(decoded_session_id)),
                                       role=decoded_role)
        except InvalidTokenError:
            raise InvalidTokenException("Error decoding access_token")
