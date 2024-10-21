from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.api.v1.schemas.session.refresh_token import RefreshTokenResponse
from app.application.user_application import UserApplication
from app.dependencies import get_user_application
from app.domain.excptions.authentication_exceptions import InvalidTokenException
from app.domain.excptions.user_exceptions import UserDoesNotExistsException
from app.domain.value_objects.tokens import AccessToken
from app.domain.value_objects.user_id import UserId
from app.logger import logger

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/{user_id}/token/refresh", response_model=RefreshTokenResponse)
def refresh_user_token(user_id: UUID,
                       user_application: UserApplication = Depends(get_user_application),
                       access_token: str = Depends(oauth2_scheme)):
    try:
        new_access_token = user_application.refresh_token(user_id=UserId(user_id),
                                                          access_token=AccessToken(access_token))
        return RefreshTokenResponse(access_token=new_access_token.access_token)
    except InvalidTokenException as e:
        logger.error(f"ERROR: User with user_id: {user_id} does not exists.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserDoesNotExistsException as e:
        logger.error(f"ERROR: User with user_id: {user_id} does not exists.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{user_id}/session/refresh", response_model=None)
def refresh_user_session():
    pass
