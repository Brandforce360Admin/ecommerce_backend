from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Response
from fastapi.security import OAuth2PasswordBearer

from app.api.v1.schemas.users.delete_user import DeleteUserResponse
from app.api.v1.schemas.users.login_user import LoginUserResponse, LoginUserRequest, UserResponseSchema
from app.api.v1.schemas.users.register_user import RegisterUserRequest, RegisterUserResponse
from app.application.user_application import UserApplication
from app.core.config import settings
from app.dependencies import get_user_application
from app.domain.excptions.authentication_exceptions import InvalidTokenException
from app.domain.excptions.user_exceptions import UserAlreadyExistsException, UserDoesNotExistsException, \
    InvalidPasswordException
from app.domain.models.users import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.password import Password
from app.domain.value_objects.tokens import AccessToken
from app.domain.value_objects.user_id import UserId
from app.logger import logger

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=RegisterUserResponse)
def register_user(user: RegisterUserRequest, user_application: UserApplication = Depends(get_user_application)):
    logger.info(f"Attempting to register user with email: {user.email}")
    try:
        new_user_api = user_application.register_user(User(name=user.name, email=user.email), Password(user.password))
        return RegisterUserResponse(user_id=new_user_api.user_id, name=new_user_api.name, email=new_user_api.email,
                                    created_at=new_user_api.created_at)
    except UserAlreadyExistsException as e:
        logger.error(f"ERROR: User with email: {user.email} already exists.")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=LoginUserResponse)
def login_user(response: Response, login_user_request: LoginUserRequest,
               user_application: UserApplication = Depends(get_user_application),
               ):
    logger.info(f"Attempting to login user with email: {login_user_request.email}")
    try:
        user, tokens = user_application.login_user(Email(login_user_request.email),
                                                   Password(login_user_request.password))
        user_details = UserResponseSchema(
            user_id=user.user_id,
            name=user.name,
            email=user.email
        )
        response.set_cookie(key="refresh_token", value=tokens.refresh_token.refresh_token, httponly=True, secure=True,
                            samesite="lax", max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRY)
        return LoginUserResponse(user_details=user_details, access_token=tokens.access_token.access_token)
    except UserDoesNotExistsException as e:
        logger.error(f"ERROR: User with email: {login_user.email} does not exists.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidPasswordException as e:
        logger.error(
            f"ERROR: User and email combination does not match for user with email: {login_user_request.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{user_id}/logout", response_model=None)
def logout_user(user_id: UUID):
    pass


@router.delete("/{user_id}/delete", response_model=None)
def delete_user(user_id: UUID, user_application: UserApplication = Depends(get_user_application),
                access_token: str = Depends(oauth2_scheme)):
    logger.info(f"Attempting to delete user with user_id: {user_id}")
    try:
        email_id = user_application.delete_user(UserId(user_id=user_id), AccessToken(access_token=access_token))
        return DeleteUserResponse(email=email_id.email)
    except InvalidTokenException as e:
        logger.error(f"ERROR: User with user_id: {user_id} does not exists.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserDoesNotExistsException as e:
        logger.error(f"ERROR: User with user_id: {user_id} does not exists.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
