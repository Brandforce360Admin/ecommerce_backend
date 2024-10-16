from app.domain.models.users import User


class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_by_email(self, user: User) -> User:
        return self.db_session.query(User).filter_by(_email=user.email).first()

    def create_user(self, user: User) -> User:
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
