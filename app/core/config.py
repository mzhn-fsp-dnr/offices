from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache
from . import config


class Settings(BaseSettings):
    PG_NAME: str
    PG_USER: str
    PG_PASS: str
    PG_HOST: str
    PG_PORT: str

    ALLOWED_ORIGINS: List[str]
    ALLOW_CREDENTIALS: bool
    ALLOW_METHODS: List[str]
    ALLOW_HEADERS: List[str]

    APP_DEBUG: bool
    APP_VERSION: str
    APP_PORT: int

    SERVICES_URL: str
    WINDOWS_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def database_link(self):
        return f"postgresql+psycopg2://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}?sslmode=disable"


@lru_cache()
def get_settings():
    return config.Settings()


conf_settings = get_settings()
