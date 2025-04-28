from __future__ import annotations

from dotenv import load_dotenv
from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

load_dotenv()


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
    )


class ServerSettings(BaseSettings):
    DEBUG: bool
    RELOAD: bool
    HOSTNAME: str
    PORT: int


server_settings = ServerSettings()


class CORSSettings(BaseSettings):
    ALLOW_ORIGINS: str
    ALLOW_CREDENTIALS: bool
    ALLOW_METHODS: str
    ALLOW_HEADERS: str


cors_settings = CORSSettings()


class LoggingSettings(BaseSettings):
    MAIN_LOGGER_NAME: str
    LOGGING_LEVEL: str = "ERROR"


logging_settings = LoggingSettings()


class DatabaseSettings(BaseSettings):
    DATABASE_ASYNC_DRIVER: str = "postgresql+asyncpg"
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str

    @property
    def async_url(self) -> str:
        return f"{self.DATABASE_ASYNC_DRIVER}://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOSTNAME}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


database_settings = DatabaseSettings()


class RedisSettings(BaseSettings):
    REDIS_HOSTNAME: str
    REDIS_PORT: int
    REDIS_CHANNEL: str

    @property
    def url(self) -> str:
        return f"redis://{self.REDIS_HOSTNAME}:{self.REDIS_PORT}"


redis_settings = RedisSettings()


class JWTSettings(BaseSettings):
    ALGORITHM: str
    SECRET_KEY: str


jwt_settings = JWTSettings()
