"""
Конфигурация приложения
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """
    Базовое описание настроек приложения.
    """

    env_file: str = ".env"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


def get_settings() -> Settings:
    """
    Фабрика для получения настройки приложения.
    """
    return Settings()
