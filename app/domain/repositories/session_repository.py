from app.domain.models.session import Session
from app.domain.value_objects.user_id import UserId


class SessionRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_session(self, session: Session) -> Session:
        self.db_session.add(session)
        self.db_session.commit()
        self.db_session.refresh(session)
        return session

    def delete_session(self, user_id: UserId):
        self.db_session.query(Session).filter_by(_user_id=user_id.user_id).delete()
        self.db_session.commit()

    def get_session(self, user_id: UserId):
        return self.db_session.query(Session).filter_by(_user_id=user_id.user_id).first()
