from typing import Tuple

from app.domain.excptions.user_exceptions import UserDoesNotExistsException
from app.domain.models.users import User
from app.domain.value_objects.tokens import GoogleUserToken, Tokens


class GoogleUserApplication:
    def __init__(self, user_service, token_service, google_service):
        self.user_service = user_service
        self.token_service = token_service
        self.google_service = google_service

    def login_google_user(self, google_token: GoogleUserToken) -> Tuple[User, Tokens]:
        email, user_name = self.google_service.validate_google_user_token(google_user_token=google_token)
        try:
            login_user = self.user_service.validate_user_existence_by_email(email)
        except UserDoesNotExistsException:
            login_user = self.user_service.create_new_user(user=User(email=email.email, name=user_name.user_name))
        tokens = self.token_service.generate_token_and_process_session(login_user)
        return login_user, tokens
