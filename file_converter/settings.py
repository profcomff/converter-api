from pydantic import BaseSettings, PostgresDsn, DirectoryPath
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    DB_DSN: PostgresDsn

    CORS_ALLOW_ORIGINS: list[str] = ['*']
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ['*']
    CORS_ALLOW_HEADERS: list[str] = ['*']

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = ".env"

    CONTENT_TYPES: List[str] = [
        'application/pdf',
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
    CONVERT_TYPES: List[str] = ['pdf']
    MAX_SIZE: int = 5000000  # Максимальный размер файла в байтах
    STATIC_FOLDER: str = DirectoryPath | None
    PRINTER_URL: str = "https://test.ru"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
