from typing import Tuple

from app.domain.models.users import User
from app.domain.services.token_service import TokenService
from app.domain.value_objects.email import Email
from app.domain.value_objects.password import Password
from app.domain.value_objects.tokens import Tokens


class UserApplication:
    def __init__(self, user_service, token_service=None):
        self.user_service = user_service
        self.token_service = token_service

    def register_user(self, user: User, password: Password) -> User:
        self.user_service.check_if_user_already_exists(user)
        new_user_application = self.user_service.create_new_user(user=user, password=password)
        return new_user_application

    def login_user(self, email: Email, password: Password) -> Tuple[User, Tokens]:
        user = self.user_service.validate_user_details(email)
        self.user_service.verify_password(user=user, plain_password=password)
        tokens = self.token_service.generate_and_persist_tokens(user)
        return user, tokens
