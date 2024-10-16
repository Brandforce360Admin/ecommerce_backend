from app.domain.models.users import User


class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_by_email(self, email: str):
        return self.db_session.query(User).filter(User.email == email).first()

    def create_user(self, user: User):
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
