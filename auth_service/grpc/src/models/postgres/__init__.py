from typing import TypeVar

from sqlalchemy.orm import declarative_base

from models.base import BaseConfig, BaseOrjsonModel

Base = declarative_base()


class SchemaInDb(BaseOrjsonModel):
    class Config(BaseConfig):
        validate_assignment = True


SchemaInDbType = TypeVar("SchemaInDbType", bound=SchemaInDb)
