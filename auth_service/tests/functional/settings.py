from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    grpc_dsn: str = Field(regex=r"^\w+:[0-9]{1,5}$")

    class Config:
        env_file = Path(__file__).parent.joinpath(".env")
        env_file_encoding = "utf-8"
        env_prefix = "test_auth_"
