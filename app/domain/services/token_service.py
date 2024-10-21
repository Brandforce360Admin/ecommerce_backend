import datetime
import secrets
import uuid
from uuid import UUID

import jwt
from jwt import InvalidTokenError

from app.core.config import settings
from app.domain.excptions.authentication_exceptions import InvalidTokenException
from app.domain.models.session import Session
from app.domain.models.users import User
from app.domain.repositories.session_repository import SessionRepository
from app.domain.value_objects.tokens import Tokens, AccessToken, RefreshToken
from app.domain.value_objects.user_id import UserId


class TokenService:
    def __init__(self, session_repository: SessionRepository):
        self.session_repository = session_repository

    def convert_uuid_to_str(self, data):
        """Recursively convert UUIDs in the data to strings."""
        if isinstance(data, dict):
            return {key: self.convert_uuid_to_str(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert_uuid_to_str(item) for item in data]
        elif isinstance(data, UUID):
            return str(data)
        return data

    def generate_access_token(self, user: User) -> AccessToken:
        secret_key = settings.JWT_SECRET
        iat_time = datetime.datetime.now(datetime.UTC)
        expiration = iat_time + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)
        payload = {
            'user_id': user.user_id,
            'role': user.role.value,
            'exp': expiration,
            'iat': iat_time
        }
        payload = self.convert_uuid_to_str(payload)

        token = jwt.encode(payload, secret_key, algorithm=settings.ALGORITHM)
        access_token = token if isinstance(token, str) else token.decode('utf-8')
        return AccessToken(access_token=access_token)

    def generate_and_persist_tokens(self, user: User, is_refresh=False) -> Tokens:
        secret_key = settings.JWT_SECRET
        iat_time = datetime.datetime.now(datetime.UTC)
        expiration = iat_time + (
            datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY) if not is_refresh else datetime.timedelta(
                days=settings.REFRESH_TOKEN_EXPIRY)
        )
        payload = {
            'user_id': user.user_id,
            'role': user.role.value,
            'exp': expiration,
            'iat': iat_time
        }
        payload = self.convert_uuid_to_str(payload)

        token = jwt.encode(payload, secret_key, algorithm=settings.ALGORITHM)
        access_token = token if isinstance(token, str) else token.decode('utf-8')
        refresh_token = secrets.token_urlsafe(32)
        session_id = uuid.uuid4()
        if not is_refresh:
            self.session_repository.create_session(
                Session(session_id=session_id, user_id=user.user_id, refresh_token=refresh_token,
                        expires_at=expiration))
        elif is_refresh:
            pass
        return Tokens(access_token=AccessToken(access_token), refresh_token=RefreshToken(refresh_token))

    @staticmethod
    def decode_token(access_token: AccessToken) -> UserId:
        secret_key = settings.JWT_SECRET
        try:
            payload = jwt.decode(access_token.access_token, secret_key, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("user_id")
            if user_id is None:
                raise InvalidTokenException("Access token does not contain user_id")
            return UserId(user_id=uuid.UUID(user_id))
        except InvalidTokenError:
            raise InvalidTokenException("Error decoding access_token")
