from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.schemas.users.login_user import LoginUserResponse, LoginUserRequest, LoginUserDetailsSchema, \
    LoginUserTokenSchema
from app.api.v1.schemas.users.register_user import RegisterUserRequest, RegisterUserResponse
from app.application.user_application import UserApplication
from app.dependencies import get_user_application
from app.domain.security.authenticate_authorise import AuthenticationAndAuthorisation
from app.domain.excptions.user_exceptions import UserAlreadyExistsException, UserDoesNotExistsException, \
    InvalidPasswordException
from app.domain.models.users import User, UserRole
from app.domain.value_objects.email import Email
from app.domain.value_objects.password import Password
from app.domain.value_objects.ids.session_id import SessionId
from app.domain.value_objects.ids.user_id import UserId
from app.logger import logger

router = APIRouter()


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
def login_user(login_user_request: LoginUserRequest,
               user_application: UserApplication = Depends(get_user_application),
               ):
    logger.info(f"Attempting to login user with email: {login_user_request.email}")
    try:
        user, tokens = user_application.login_user(Email(login_user_request.email),
                                                   Password(login_user_request.password))
        user_details = LoginUserDetailsSchema(
            user_id=user.user_id,
            name=user.name,
            email=user.email
        )
        tokens = LoginUserTokenSchema(
            access_token=tokens.access_token.access_token,
            refresh_token=tokens.refresh_token.refresh_token
        )

        return LoginUserResponse(user_details=user_details, tokens=tokens)
    except UserDoesNotExistsException as e:
        logger.error(f"ERROR: User with email: {login_user_request.email} does not exists.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidPasswordException as e:
        logger.error(
            f"ERROR: User and email combination does not match for user with email: {login_user_request.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{user_id}/logout")
def logout_user(user_id: UUID, session_id: SessionId = Depends(AuthenticationAndAuthorisation(UserRole.customer)),
                user_application: UserApplication = Depends(get_user_application)):
    logger.info(f"Attempting to logout user with user_id: {user_id}")
    user_application.logout_user(user_id=UserId(user_id=user_id), session_id=session_id)

@router.delete("/{user_id}/delete")
def delete_user(user_id: UUID, session_id: SessionId = Depends(AuthenticationAndAuthorisation(UserRole.customer)),
                user_application: UserApplication = Depends(get_user_application)):
    logger.info(f"Attempting to delete user with user_id: {user_id}")
    user_application.delete_user(user_id=UserId(user_id))
