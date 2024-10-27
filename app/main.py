import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.endpoints.sessions import session
from app.api.v1.endpoints.users import user
from app.core.config import settings
from app.db.base import Base, engine
from app.domain.excptions.authentication_exceptions import InvalidTokenException, TokenExpiredException, \
    UserAccessException, UserNonLoggedInException

app = FastAPI()


@app.exception_handler(InvalidTokenException)
def invalid_token_exception_handler(request: Request, exc: InvalidTokenException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(TokenExpiredException)
def token_expiration_exception_handler(request: Request, exc: TokenExpiredException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(UserAccessException)
def user_access_exception_handler(request: Request, exc: UserAccessException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(UserNonLoggedInException)
def user_not_logged_exception_handler(request: Request, exc: UserNonLoggedInException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


# metadata = MetaData(schema=settings.USER_SCHEMA)
Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix=f"{settings.BASE_URL}/v1/users", tags=["Users"])
app.include_router(session.router, prefix=f"{settings.BASE_URL}/v1/users", tags=["Session"])


@app.get("/")
def read_root():
    return {"message": f"Welcome to the FastAPI app!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
