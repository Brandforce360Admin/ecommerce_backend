from fastapi import APIRouter, Depends, HTTPException, status

from app.application.user_application import UserApplication
from app.dependencies import get_user_application
from app.domain.excptions.user_exceptions import UserAlreadyExistsException
from app.domain.models.users import User
from app.domain.value_objects.password import Password
from app.api.v1.schemas.users.register_user import UserCreate, UserResponse
from app.logger import logger

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, user_application: UserApplication = Depends(get_user_application)):
    logger.info(f"Attempting to register user with email: {user.email}")
    try:
        new_user_api = user_application.register_user(User(name=user.name, email=user.email), Password(user.password))
        return UserResponse(user_id=new_user_api.user_id, name=new_user_api.name, email=new_user_api.email,
                            created_at=new_user_api.created_at)
    except UserAlreadyExistsException as e:
        logger.error(f"ERROR: User with email: {user.email} already exists.")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
