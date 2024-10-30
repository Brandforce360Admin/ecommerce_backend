from typing import Tuple

from google.auth.transport import requests
from google.oauth2 import id_token

from app.core.config import settings
from app.domain.excptions.authentication_exceptions import InvalidGoogleTokenException
from app.domain.value_objects.email import Email
from app.domain.value_objects.tokens import GoogleUserToken
from app.domain.value_objects.username import UserName


class GoogleService:
    @staticmethod
    def validate_google_user_token(google_user_token: GoogleUserToken) -> Tuple[Email, UserName]:
        try:
            id_info = id_token.verify_oauth2_token(google_user_token.google_user_token, requests.Request(),
                                                   settings.GOOGLE_CLIENT_ID)
            return Email(email=id_info["email"]), UserName(user_name=id_info["name"])

        except ValueError:
            raise InvalidGoogleTokenException("Invalid Google Token")
