from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SERVER: str
    BUCKET: str
    BUCKET_FACE: str
    BUCKET_PLATE: str

    MONGO_DATABASE: str
    MONGO_DATABASE_URI: str

    MULTI_MAX: int = 20

    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    HOST_MAIN_SERVER: str

    ENVIRONMENT: str
    REQUEST_TIMEOUT: int = 5
    HIK_FACE_LIB_ID: Optional[int] = None
    HIK_NOTI_CHANNEL: Optional[int] = None
    SERVER_PORT: int = 8000

    def __init__(self, **data):
        super().__init__(**data)
        if self.ENVIRONMENT == "dev":
            self.HIK_FACE_LIB_ID = 1
            self.HIK_NOTI_CHANNEL = 1
        elif self.ENVIRONMENT == "staging":
            self.HIK_FACE_LIB_ID = 2
            self.HIK_NOTI_CHANNEL = 2
        elif self.ENVIRONMENT == "prod":
            self.HIK_FACE_LIB_ID = 3
            self.HIK_NOTI_CHANNEL = 3


settings = Settings()
