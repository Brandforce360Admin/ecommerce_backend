import uvicorn
from fastapi import FastAPI

from app.api.v1.endpoints.session import session
from app.api.v1.endpoints.users import user
from app.core.config import settings
from app.db.base import Base, engine

app = FastAPI()

# metadata = MetaData(schema=settings.USER_SCHEMA)
Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix=f"{settings.BASE_URL}/v1/users", tags=["Users"])
app.include_router(session.router, prefix=f"{settings.BASE_URL}/v1/users", tags=["Session"])


@app.get("/")
def read_root():
    return {"message": f"Welcome to the FastAPI app!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)