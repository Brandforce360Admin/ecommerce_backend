from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.user_application import UserApplication
from app.db.base import get_db
from app.domain.repositories.session_repository import SessionRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.token_service import TokenService
from app.domain.services.user_service import UserService


def get_user_repository(db_session: Session = Depends(get_db)):
    return UserRepository(db_session)


def get_session_repository(db_session: Session = Depends(get_db)):
    return SessionRepository(db_session)


def get_token_service(session_repository: SessionRepository = Depends(get_session_repository)):
    return TokenService(session_repository)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)


def get_user_application(user_service: UserService = Depends(get_user_service),
                         token_service: Optional[TokenService] = Depends(get_token_service)):
    return UserApplication(user_service, token_service)
