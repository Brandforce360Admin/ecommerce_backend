from sqlalchemy.orm import Session
from app.domain.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def create_new_user(db: Session, user_in: UserCreate):
    user = UserRepository.get_by_email(db, email=user_in.email)
    if user:
        raise ValueError("User already registered")

    hashed_password = get_password_hash(user_in.password)
    return UserRepository.create_user(db, user=user_in, hashed_password=hashed_password)
