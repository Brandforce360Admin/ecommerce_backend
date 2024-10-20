from app.domain.models.session import Session


class SessionRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_session(self, session: Session) -> Session:
        self.db_session.add(session)
        self.db_session.commit()
        self.db_session.refresh(session)
        return session
