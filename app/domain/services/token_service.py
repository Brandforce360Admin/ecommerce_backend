import datetime
import uuid
from uuid import UUID

import jwt

from app.core.config import settings
from app.domain.models.users import User
from app.domain.services.session_service import SessionService
from app.domain.value_objects.expiry import Expiry
from app.domain.value_objects.session_id import SessionId
from app.domain.value_objects.tokens import Tokens, AccessToken, RefreshToken


class TokenService:
    def __init__(self, session_service: SessionService):
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
        refresh_token_expiration = iat_time + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRY)
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
            self.session_service.update_session_for_user(session_id=SessionId(session_id), user=user,
                                                         refresh_token=refresh_token,
                                                         expiry=Expiry(refresh_token_expiration))
        else:
            self.session_service.create_session_for_user(session_id=SessionId(session_id), user=user,
                                                         refresh_token=refresh_token,
                                                         expiry=Expiry(refresh_token_expiration))

        return Tokens(access_token=AccessToken(access_token), refresh_token=refresh_token)
