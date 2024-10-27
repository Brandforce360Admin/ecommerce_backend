from typing import Tuple

from app.domain.models.users import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.password import Password
from app.domain.value_objects.session_id import SessionId
from app.domain.value_objects.tokens import Tokens, AccessToken
from app.domain.value_objects.user_id import UserId


class UserApplication:
    def __init__(self, user_service, token_service=None, session_service=None):
        self.user_service = user_service
        self.token_service = token_service
        self.session_service = session_service

    def register_user(self, user: User, password: Password) -> User:
        self.user_service.check_if_user_already_exists(user)
        new_user = self.user_service.create_new_user(user=user, password=password)
        return new_user

    def login_user(self, email: Email, password: Password) -> Tuple[User, Tokens]:
        user = self.user_service.validate_user_existence_by_email(email)
        self.user_service.verify_password(user=user, plain_password=password)
        tokens = self.token_service.generate_token_and_process_session(user)
        return user, tokens

    def logout_user(self, user_id: UserId, session_id: SessionId):
        self.session_service.delete_session_for_user(user_id=user_id, session_id=session_id)

    def delete_user(self, user_id: UserId):
        self.session_service.delete_all_sessions_for_user(user_id)
        self.user_service.delete_user_by_id(user_id=user_id)

    def refresh_token(self, user_id: UserId, access_token: AccessToken):
        authenticated_user = self.user_service.authenticate_user(user_id, access_token)
        return self.token_service.generate_token_and_process_session(user=authenticated_user)

    def refresh_session(self):
        pass
    #
    # def authenticate_user(self, user_id: UserId, access_token: AccessToken):
    #     return self.user_service.authenticate_user(user_id, access_token)
