import logging

import uvicorn
from fastapi import FastAPI

from app.api.v1.endpoints import user
from app.core.config import settings
from app.db.base import Base, engine

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix=f"{settings.BASE_URL}/v1/users", tags=["Users"])


@app.get("/")
def read_root():
    return {"message": f"Welcome to the FastAPI app!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)