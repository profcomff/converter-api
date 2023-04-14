from pydantic import BaseSettings, DirectoryPath
from functools import lru_cache
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""

    CORS_ALLOW_ORIGINS: list[str] = ['*']
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ['*']
    CORS_ALLOW_HEADERS: list[str] = ['*']
    ROOT_PATH: str = '/' + os.getenv('APP_NAME', '')
    EXTENTIONS: List[str] = ['pdf', 'docx', 'doc']
    CONVERT_TYPES: List[str] = ['pdf']
    MAX_SIZE: int = 5000000  # Максимальный размер файла в байтах
    STATIC_FOLDER: DirectoryPath | None

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
