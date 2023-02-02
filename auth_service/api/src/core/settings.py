from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, BaseModel, RedisDsn, Field

PROJECT_DIR = Path(__file__).parent.parent


class Jaeger(BaseModel):
    host: str
    port: int
    header: str
    service_name: str


class BlueprintRateLimit(BaseModel):
    user: str | None
    admin: str | None
    auth: str | None


class RateLimitSettings(BaseModel):
    default: str
    endpoint_signup: str | None
    blueprint: BlueprintRateLimit | None


class Settings(BaseSettings):
    testing: bool
    host: str
    grpc_dsn: str = Field(regex=r"^\w+:[0-9]{1,5}$")
    rate_limit_redis_dsn: RedisDsn = Field(..., env="auth_api_redis_dsn")
    log_level: str
    log_folder: Path | None
    rate_limit: RateLimitSettings
    jaeger: Jaeger

    class Config:
        env_prefix = "auth_api_"
        env_nested_delimiter = "__"
        case_sensitive = False
        env_file = PROJECT_DIR.parent.joinpath(".env")
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
