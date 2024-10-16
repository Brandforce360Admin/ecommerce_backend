import logging

from fastapi import FastAPI

from app.api.v1.endpoints import user
from app.api.v1.exception_handlers.user_exception_handlers import user_already_exists_exception_handler
from app.core.config import settings
from app.db.base import Base, engine
from app.domain.excptions.user_exceptions import UserAlreadyExistsException

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app.add_exception_handler(UserAlreadyExistsException, user_already_exists_exception_handler)
app.include_router(user.router, prefix=f"{settings.BASE_URL}/v1/users", tags=["Users"])


@app.get("/")
def read_root():
    return {"message": f"Welcome to the FastAPI app!"}
