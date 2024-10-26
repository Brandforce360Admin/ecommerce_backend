import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.domain.excptions.authentication_exceptions import InvalidTokenException
from app.domain.excptions.user_exceptions import UserAlreadyExistsException, UserDoesNotExistsException, \
    InvalidPasswordException, UserNonLoggedInException
from app.domain.models.users import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.token_service import TokenService
from app.domain.value_objects.email import Email
from app.domain.value_objects.password import Password
from app.domain.value_objects.tokens import AccessToken
from app.domain.value_objects.user_id import UserId
from app.logger import logger


class UserService:
    def __init__(self, user_repository: UserRepository, token_service: TokenService):
        self.user_repository = user_repository
        self.token_service = token_service

    def check_if_user_already_exists(self, user: User):
        user = self.user_repository.get_by_email(Email(user.email))
        if user is not None:
            logger.error(f"ERROR: User with email: {user.email} already exists.")
            raise UserAlreadyExistsException(f"User with {user.email} already exists.")

    def validate_user_details(self, email: Email) -> User:
        user = self.user_repository.get_by_email(email)
        if user is None:
            logger.info(f"INFO: User with email: {email.email} already exists.")
            raise UserDoesNotExistsException(f"User with {email.email} does not exists.")
        return user

    def create_new_user(self, user: User, password: Password) -> User:
        user.password_hash = PasswordHasher().hash(password.password)
        user.created_at = datetime.datetime.now(datetime.UTC)
        new_user = self.user_repository.create_user(user)
        return new_user

    def delete_user(self, user: User):
        self.token_service.delete_session(user)
        self.user_repository.delete_user(user)

    def logout_user(self, user: User):
        self.token_service.delete_session(user)

    def get_user_details_by_id(self, user_id: UserId) -> User:
        return self.user_repository.get_by_id(user_id)

    @staticmethod
    def verify_password(user: User, plain_password: Password):
        try:
            PasswordHasher().verify(user.password_hash, plain_password.password)
        except VerifyMismatchError as e:
            logger.info("INFO: Password hash do not match")
            raise InvalidPasswordException("INFO: Password hash do not match")

    def authenticate_user(self, user_id: UserId, access_token: AccessToken) -> User:
        decoded_user_id, decoded_session_id, decoded_role = self.token_service.decode_and_authenticate_token(
            access_token=access_token)
        if not decoded_user_id.user_id == user_id.user_id:
            raise InvalidTokenException(f"Token is invalid for user_id {user_id.user_id}")
        user_session = self.token_service.get_session_by_user_id(user_id=user_id)
        if user_session is None:
            raise UserNonLoggedInException(f"User with user_id {user_id.user_id} is not logged in")
        user_details = self.get_user_details_by_id(user_id)
        if user_details is None:
            raise UserDoesNotExistsException(f"User with user_id {user_id.user_id} does not exists")
        return user_details
