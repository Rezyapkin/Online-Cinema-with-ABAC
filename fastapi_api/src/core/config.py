from functools import lru_cache
from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings, RedisDsn, AnyHttpUrl, BaseModel, Field

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = Path(__file__).parent.parent


class Jaeger(BaseModel):
    host: str
    port: int
    header: str
    service_name: str


class Settings(BaseSettings):
    testing: bool
    redis_dsn: RedisDsn
    default_cache_ttl: int
    elasticsearch_dsn: AnyHttpUrl
    auth_service_dsn: str | None = Field(regex=r"^\w+:[0-9]{1,5}$")
    jaeger: Jaeger

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_validate()

    def post_validate(self):
        if self.testing is False:
            if not self.auth_service_dsn:
                raise ValueError("Auth service must be configured in production mode!")

    class Config:
        env_nested_delimiter = "__"
        env_prefix = "fastapi_api_"
        env_file = BASE_DIR.parent.joinpath(".env")
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
