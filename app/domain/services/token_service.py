import datetime
import secrets
import uuid
from uuid import UUID

import jwt

from app.core.config import settings
from app.domain.models.session import Session
from app.domain.models.users import User
from app.domain.repositories.session_repository import SessionRepository
from app.domain.value_objects.tokens import Tokens


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
        self.session_repository.create_session(
            Session(session_id=session_id, user_id=user.user_id, refresh_token=refresh_token, expires_at=expiration))
        return Tokens(access_token=access_token, refresh_token=refresh_token)
