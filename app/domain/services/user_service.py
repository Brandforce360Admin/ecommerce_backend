import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.domain.excptions.user_exceptions import UserAlreadyExistsException, UserDoesNotExistsException, \
    InvalidPasswordException
from app.domain.models.users import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.email import Email
from app.domain.value_objects.password import Password
from app.logger import logger


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

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

    @staticmethod
    def verify_password(user: User, plain_password: Password):
        try:
            PasswordHasher().verify(user.password_hash, plain_password.password)
        except VerifyMismatchError as e:
            logger.info("INFO: Password hash do not match")
            raise InvalidPasswordException("INFO: Password hash do not match")
