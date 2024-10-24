import uuid

from app.domain.models.session import Session
from app.domain.models.users import User
from app.domain.repositories.session_repository import SessionRepository
from app.domain.value_objects.expiry import Expiry
from app.domain.value_objects.session_id import SessionId
from app.domain.value_objects.tokens import RefreshToken


class SessionService:
    def __init__(self, session_repository: SessionRepository):
        self.session_repository = session_repository

    def create_session_for_user(self, user: User, refresh_token: RefreshToken, expiry: Expiry):
        self.session_repository.create_session(
            Session(session_id=uuid.uuid4(), user_id=user.user_id, refresh_token=refresh_token.refresh_token,
                    expires_at=expiry.expiry))

    def update_session_for_user(self, user: User, refresh_token: RefreshToken, expiry: Expiry):
        pass

    def get_user_session_by_id(self, user: User, session_id: SessionId):
        pass

    def get_all_user_sessions(self, user: User):
        pass

    def delete_session_for_user(self, user: User, session_id: SessionId):
        pass

    def delete_all_sessions_for_user(self, user: User):
        pass
