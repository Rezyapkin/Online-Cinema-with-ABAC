"""
Utility functions and classes for ABAC.
"""
from pydantic import BaseModel

import orjson


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseConfig:
    json_loads = orjson.loads
    json_dumps = orjson_dumps


class BaseOrjsonModel(BaseModel):
    class Config(BaseConfig):
        pass


class PrettyPrint:
    """
    Allows to log objects with all the fields
    """

    def __str__(self) -> str:
        return f"{self.__class__} <Object ID {id(self)}>: {vars(self)}"
