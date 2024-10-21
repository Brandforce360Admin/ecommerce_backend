from app.domain.models.users import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId


class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_by_email(self, email: Email) -> User:
        return self.db_session.query(User).filter_by(_email=email.email).first()

    def get_by_id(self, user_id: UserId) -> User:
        return self.db_session.query(User).filter_by(_user_id=user_id.user_id).first()

    def create_user(self, user: User) -> User:
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
