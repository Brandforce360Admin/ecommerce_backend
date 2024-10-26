import datetime
import uuid
from typing import Tuple
from uuid import UUID

import jwt
from jwt import InvalidTokenError

from app.core.config import settings
from app.domain.excptions.authentication_exceptions import InvalidTokenException, TokenExpiredException
from app.domain.models.users import User, UserRole
from app.domain.repositories.session_repository import SessionRepository
from app.domain.services.session_service import SessionService
from app.domain.value_objects.expiry import Expiry
from app.domain.value_objects.session_id import SessionId
from app.domain.value_objects.tokens import Tokens, AccessToken, RefreshToken
from app.domain.value_objects.user_id import UserId


class TokenService:
    def __init__(self, session_repository: SessionRepository, session_service: SessionService):
        self.session_repository = session_repository
        self.session_service = session_service

    def convert_uuid_to_str(self, data):
        """Recursively convert UUIDs in the data to strings."""
        if isinstance(data, dict):
            return {key: self.convert_uuid_to_str(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert_uuid_to_str(item) for item in data]
        elif isinstance(data, UUID):
            return str(data)
        return data

    def generate_token_and_process_session(self, user: User, is_refresh=None) -> Tokens:
        secret_key = settings.JWT_SECRET
        iat_time = datetime.datetime.now(datetime.UTC)
        access_token_expiration = iat_time + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)
        refresh_token_expiration = iat_time + datetime.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRY)
        session_id = uuid.uuid4()
        access_token_payload = {
            'user_id': user.user_id,
            'role': user.role.value,
            'exp': access_token_expiration,
            'session_id': session_id,
            'iat': iat_time
        }
        refresh_token_payload = {
            'user_id': user.user_id,
            'role': user.role.value,
            'exp': refresh_token_expiration,
            'session_id': session_id,
            'iat': iat_time
        }
        access_token_payload = self.convert_uuid_to_str(access_token_payload)
        refresh_token_payload = self.convert_uuid_to_str(refresh_token_payload)

        access_token = jwt.encode(access_token_payload, secret_key, algorithm=settings.ALGORITHM)
        refresh_token = jwt.encode(refresh_token_payload, secret_key, algorithm=settings.ALGORITHM)
        refresh_token = RefreshToken(refresh_token=refresh_token)
        if is_refresh:
            self.session_service.update_session_for_user(user=user,
                                                         refresh_token=refresh_token,
                                                         expiry=Expiry(refresh_token_expiration))
        else:
            self.session_service.create_session_for_user(user=user,
                                                         refresh_token=refresh_token,
                                                         expiry=Expiry(refresh_token_expiration))

        return Tokens(access_token=AccessToken(access_token), refresh_token=refresh_token)

    @staticmethod
    def decode_and_authenticate_token(access_token: AccessToken) -> Tuple[UserId, SessionId, UserRole]:
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
            session_id: str = payload.get("session_id")
            if session_id is None:
                raise InvalidTokenException("Access token does not contain session_id")
            return UserId(user_id=uuid.UUID(user_id)), SessionId(session_id=uuid.UUID(session_id)), UserRole[role]
        except InvalidTokenError:
            raise InvalidTokenException("Error decoding access_token")
