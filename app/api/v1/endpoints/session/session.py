from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.api.v1.schemas.session.refresh_token import RefreshTokenRequest
from app.api.v1.schemas.users.login_user import TokenSchema
from app.application.user_application import UserApplication
from app.dependencies import get_user_application
from app.domain.excptions.user_exceptions import UserAlreadyExistsException
from app.domain.value_objects.tokens import AccessToken
from app.domain.value_objects.user_id import UserId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/refresh", response_model=TokenSchema)
def refresh_user_tokens(refresh_token: RefreshTokenRequest,
                        user_application: UserApplication = Depends(get_user_application),
                        token: str = Depends(oauth2_scheme)):
    try:
        user_application.refresh_token(user_id=UserId(refresh_token.user_id), access_token=AccessToken(token))
    except UserAlreadyExistsException as e:

        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
