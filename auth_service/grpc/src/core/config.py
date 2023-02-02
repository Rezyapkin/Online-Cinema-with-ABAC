from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, BaseModel, PostgresDsn, RedisDsn, Field, HttpUrl

# Корень проекта
BASE_DIR = Path(__file__).parent.parent


class Jaeger(BaseModel):
    host: str
    port: int
    service_name: str


class OAuthProviderSettings(BaseModel):
    authorization_url: HttpUrl
    client_id: str
    client_secret: str
    scope: str
    token_url: HttpUrl


class OpenIdOAuthProviderSettings(OAuthProviderSettings):
    check_id_token_url: HttpUrl


class OAuthYandexSettings(OAuthProviderSettings):
    user_info_url: HttpUrl


class OAuthProviders(BaseModel):
    google: OpenIdOAuthProviderSettings
    yandex: OAuthYandexSettings


class Settings(BaseSettings):
    testing: bool
    postgres_dsn: PostgresDsn
    redis_dsn: RedisDsn
    default_cache_ttl: int = Field(default=10)
    secret_key: str
    log_level: str
    log_folder: str
    log_file: str
    jaeger: Jaeger
    oauth: OAuthProviders

    class Config:
        env_nested_delimiter = "__"
        env_prefix = "auth_grpc_"
        env_file = BASE_DIR.parent.joinpath(".env")
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
