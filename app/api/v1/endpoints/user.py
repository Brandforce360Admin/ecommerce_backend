from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.domain.excptions.user_exceptions import UserAlreadyExistsException
from app.schemas.user import UserCreate, UserResponse
from app.domain.services import create_new_user

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_new_user(db=db, user_in=user)
        return new_user
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))
