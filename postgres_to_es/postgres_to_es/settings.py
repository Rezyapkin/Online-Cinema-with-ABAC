from pydantic import BaseModel, BaseSettings, PostgresDsn, RedisDsn, AnyHttpUrl


class ElkIndexes(BaseModel):
    movies: str
    movies_file: str
    persons: str
    persons_file: str
    genres: str
    genres_file: str


class Settings(BaseSettings):
    postgres_dsn: PostgresDsn
    extract_chunk: int
    redis_dsn: RedisDsn
    elasticsearch_dsn: AnyHttpUrl
    elasticsearch_indexes: ElkIndexes
    load_chunk: int

    class Config:
        env_prefix = "etl_movies_"
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
