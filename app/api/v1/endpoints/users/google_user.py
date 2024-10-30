from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.schemas.users.google_login_user import GoogleLoginRequest
from app.api.v1.schemas.users.login_user import LoginUserDetailsSchema, LoginUserTokenSchema, LoginUserResponse
from app.application.google_user_application import GoogleUserApplication
from app.dependencies import get_google_user_application
from app.domain.excptions.authentication_exceptions import InvalidGoogleTokenException
from app.domain.value_objects.tokens import GoogleUserToken

router = APIRouter()


@router.post("/login")
def google_login(google_login_user_request: GoogleLoginRequest,
                 google_user_application: GoogleUserApplication = Depends(get_google_user_application)):
    try:
        user, tokens = google_user_application.login_google_user(GoogleUserToken(google_login_user_request.token))
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
    except InvalidGoogleTokenException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
