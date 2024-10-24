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
from app.domain.services.session_service import SessionService
from app.domain.value_objects.expiry import Expiry
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

    def delete_session(self, user: User):
        self.session_repository.delete_session(UserId(user_id=user.user_id))

    def get_session_by_user_id(self, user_id: UserId):
        return self.session_repository.get_session(user_id)

    def generate_tokens(self, user: User, is_refresh=False) -> Tokens:
        secret_key = settings.JWT_SECRET
        iat_time = datetime.datetime.now(datetime.UTC)
        expiration = iat_time + (
            datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY) if not is_refresh else datetime.timedelta(
                days=settings.REFRESH_TOKEN_EXPIRY)
        )
        access_token_payload = {
            'user_id': user.user_id,
            'role': user.role.value,
            'exp': expiration,
            'iat': iat_time
        }
        payload = self.convert_uuid_to_str(payload)

        access_token = jwt.encode(payload, secret_key, algorithm=settings.ALGORITHM)
        refresh_token = jwt.encode(payload, secret_key, algorithm=settings.ALGORITHM)
        access_token = access_token if isinstance(access_token, str) else access_token.decode('utf-8')
        refresh_token = access_token if isinstance(access_token, str) else access_token.decode('utf-8')
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
