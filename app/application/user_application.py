from app.domain.models.users import User
from app.domain.value_objects.password import Password


class UserApplication:
    def __init__(self, user_service):
        self.user_service = user_service

    def register_user(self, user: User, password: Password) -> User:
        self.user_service.check_if_user_already_exists(user)
        new_user_application =  self.user_service.create_new_user(user, password)
        return new_user_application
