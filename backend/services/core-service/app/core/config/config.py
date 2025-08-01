from functools import lru_cache
from pathlib import Path
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")

    if ENVIRONMENT == "local":
        RABBITMQ_URL: str = "amqp://guest:guest@localhost/"  # local
        DATABASE_URL: str = "postgresql://postgres:admin@localhost/fitplan_db"  # local
        IAM_URL: str = "http://iam.localhost"  # local

    elif ENVIRONMENT == "docker":
        RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq/"  # docker
        DATABASE_URL: str = "postgresql://postgres:admin@postgres_container:5432/fitplan_db"  # docker
        IAM_URL: str = "http://iam"  # docker

    # *************************
    # # DATABASE_URL: str = "mongodb://mongo:27017"
    # DATABASE_URL: str = "mongodb://localhost:27017"
    # DATABASE_NAME: str = "FitPlanMediaDB"
    # TESSERACT_CMD: str = ""
    # MEDIA_SERVICE_GRPC: str = ""
    # # REDIS_URL: str = "localhost"
    # REDIS_URL: str = "redis"
    # JWT_SECRET_KEY: str = "1807372bcbf0963ebe30a1df3669690b8f0e4f83a1b52e7579cfee9ff08db230"
    # JWT_ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # OTP_EXPIRE_TIME: int = 60
    # # *************************
    # SMTP_SERVER: str = "smtp.gmail.com"
    # SMTP_PORT: int = 465
    # SMTP_USERNAME: str = "asldy3097@gmail.com"
    # SMTP_PASSWORD: str = "xrtwqctuprcgeiyj"
    # EMAIL_FROM: str = "asldy3097@gmail.com"
    # model_config = SettingsConfigDict(env_file=str(Path(__file__).resolve().parent / ".env"))
    # *****************************************************
    FitPlAN_PRICE: int = 1000000


@lru_cache
@logger.catch
def get_settings():
    return Settings()
