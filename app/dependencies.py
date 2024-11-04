from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.cart_application import CartApplication
from app.application.google_user_application import GoogleUserApplication
from app.application.user_application import UserApplication
from app.db.base import get_db
from app.domain.repositories.session_repository import SessionRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.google_service import GoogleService
from app.domain.services.session_service import SessionService
from app.domain.services.token_service import TokenService
from app.domain.services.user_service import UserService


def get_user_repository(db_session: Session = Depends(get_db)):
    return UserRepository(db_session)


def get_session_repository(db_session: Session = Depends(get_db)):
    return SessionRepository(db_session)


def get_session_service(session_repository: SessionRepository = Depends(get_session_repository)):
    return SessionService(session_repository)


def get_token_service(session_service: SessionService = Depends(get_session_service)):
    return TokenService(session_service)


def get_google_service():
    return GoogleService()


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)


def get_user_application(user_service: UserService = Depends(get_user_service),
                         token_service: Optional[TokenService] = Depends(get_token_service),
                         session_service: Optional[SessionService] = Depends(get_session_service)):
    return UserApplication(user_service, token_service, session_service)


def get_cart_application():
    return CartApplication()


def get_google_user_application(user_service: UserService = Depends(get_user_service),
                                token_service: TokenService = Depends(get_token_service),
                                google_service: TokenService = Depends(get_google_service)):
    return GoogleUserApplication(user_service, token_service, google_service)
