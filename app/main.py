from fastapi import FastAPI

from app.api.v1.endpoints import user
from app.core.config import settings

app = FastAPI()

app.include_router(user.router, prefix=f"{settings.BASE_URL}/v1/users", tags=["Users"])


@app.get("/")
def read_root():
    return {"message": f"Welcome to the FastAPI app!"}
