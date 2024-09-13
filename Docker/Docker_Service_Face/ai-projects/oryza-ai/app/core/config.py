import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    # services configurations
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        43200  # 60 * 24, 1 day #TODO: change to 5 minutes
    )
    # JWT

    REQUEST_TIMEOUT: int = 5  # seconds
    EMAILS_ENABLED: bool = False

    MULTI_MAX: int = 20

    # COMPONENT SETTINGS
    MONGO_DATABASE: str
    MONGO_DATABASE_URI: str

    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_USERNAME: str
    FIRST_SUPERUSER_PASSWORD: str

    FIRST_USER_EMAIL: EmailStr
    FIRST_USER_USERNAME: str
    FIRST_USER_PASSWORD: str

    # rabbitmq
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_EXCHANGE_TYPE: str
    SERVER_FACE: str

    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SERVER: str
    BUCKET: str

    # SETTING DETECT ITEMS FORGOTTEN
    DIFS_BOUNDARY: str = "[[0,0],[1,0],[1,1],[0,1]]"
    DIFS_WAITING_TIME: int = 3  # 3 seconds

    # SETTING IDENTIFY UNIFORMS
    IUS_BOUNDARY: str = "[[0,0],[1,0],[1,1],[0,1]]"
    IUS_WAITING_TIME: int = 3  # 3 seconds
    IUS_RGB: str = "[101,113,124]"

    # SETTING LOITERING DETECTION
    LD_BOUNDARY: str = "[[0,0],[1,0],[1,1],[0,1]]"
    LD_WAITING_TIME: int = 10  # 10 seconds
    ENVIRONMENT: str

    # SETTING ILLEGAL PARKING
    IP_BOUNDARY: str = "[[0,0],[1,0],[1,1],[0,1]]"
    IP_WAITING_TIME: int = 10  # 10 seconds
    IP_ALERT_INTERVAL: int = 60  # 60 seconds

    # SETTING TRIPWIRE
    TW_LINE: str = "[[0.5,0],[0.5,1]]"

    VMS_RTSP_PORT: int = 8554
    VMS_PUSH_PORT: int = 8080

    # VIDEO ANALYZE SERVERS
    SERVER_VIDEO_ANALYZE_PLATE: str
    SERVER_VIDEO_ANALYZE_FACE: str
    VIDEO_ESTIMATE_REQUEST_TIMEOUT: int = 5  # seconds

    # HLS STREAM
    HLS_STREAM_PORT: int = 8888


settings = Settings()
