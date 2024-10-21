import os

from dotenv import load_dotenv
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRY: int = int(os.getenv("ACCESS_TOKEN_EXPIRY"))
    REFRESH_TOKEN_EXPIRY: int = int(os.getenv("ACCESS_TOKEN_EXPIRY"))
    BASE_URL: str = os.getenv("BASE_URL")
    USER_SCHEMA: str = os.getenv("USER_SCHEMA")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL")
    JWT_SECRET: str = os.getenv("JWT_SECRET")

    model_config = ConfigDict(env_file=".env")


settings = Settings()
