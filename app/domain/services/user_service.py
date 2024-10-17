import datetime

from passlib.context import CryptContext

from app.domain.excptions.user_exceptions import UserAlreadyExistsException
from app.domain.models.users import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.password import Password
from argon2 import PasswordHasher

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def check_if_user_already_exists(self, user: User):
        user = self.user_repository.get_by_email(user)
        if user is not None:
            raise UserAlreadyExistsException(f"User with {user.email} already exists.")

    def create_new_user(self, user: User, password: Password) -> User:
        user.password_hash = PasswordHasher().hash(password.password)
        user.created_at = datetime.datetime.now(datetime.UTC)
        new_user = self.user_repository.create_user(user)
        return new_user
