from abc import abstractmethod, ABC
from datetime import date, datetime
from functools import wraps
from itertools import chain
from typing import Callable, Any, Coroutine
from uuid import UUID

from pydantic import BaseModel

from db.base import AbstractAsyncStorage
from models.base import BaseOrjsonModel


class BaseAsyncCacheStorage(AbstractAsyncStorage, ABC):
    """Abstract class for caching Pydantic-model."""

    @abstractmethod
    async def set(self, key: str, value: BaseOrjsonModel, ttl: int) -> None:
        """
        An abstract set method that should store the value of the
        Pydantic model in the child class by the specified key.
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str, model_type: type[BaseOrjsonModel]) -> BaseOrjsonModel | None:
        """An abstract get method that should return the Pydantic model from the key storage in the child class."""
        raise NotImplementedError

    @classmethod
    def serialize_cached_function_param(cls, param: any, separator_for_mapping_param: str = "___") -> str | None:
        """
        Serializes parameters of arbitrary type in str if possible. If it is not possible, None is returned.

        :param param: the value of the parameter to be serialized;
        :param separator_for_mapping_param: separator for serialization of child parameter fields;
        :return: a parameter serialized to a string or None if serialization is not possible.
        """
        if isinstance(param, (str, int, float, UUID)):
            return str(param)
        elif isinstance(param, (date, datetime)):
            return param.isoformat()
        elif isinstance(param, (dict, BaseModel)) and len(separator_for_mapping_param) < 10:
            if isinstance(param, BaseModel):
                param = param.dict()
            keys_values = []
            for key, value in param.items():
                serialized_value = cls.serialize_cached_function_param(value, separator_for_mapping_param + "_")
                if serialized_value is None:
                    continue
                keys_values.append(f"{key} === {serialized_value}")
            return separator_for_mapping_param.join(keys_values)

        return None

    @classmethod
    def get_cache_key(cls, func: callable, *args, **kwargs) -> str:
        """
        Returns the key value by the function name and the value of its parameters.
        The key contains only parameters that have one of the types: str, int, float, date, datetime.
        """
        prefix_cache_key = ".".join([func.__module__, func.__qualname__])
        params_cache_key = [
            cls.serialize_cached_function_param(func_param) for func_param in chain(args, kwargs.values())
        ]
        return "__".join(chain([prefix_cache_key], [key for key in params_cache_key if key is not None]))

    def cache_decorator(
        self, model_type: type[BaseOrjsonModel], ttl: int
    ) -> Callable[[..., BaseOrjsonModel], Callable]:
        """
        A decorator that caches the values of the Pydantic-model functions in the specified storage and,
        if available, retrieves the values from the cache.

        :param model_type: Pydantic model Class for parsing;
        :param ttl: duration of record caching in seconds;
        :return: wrap-function.
        """

        def _decorator(
            method: Callable,
        ) -> Callable[[tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, BaseOrjsonModel]]:
            @wraps(method)
            async def _method(*args, **kwargs) -> BaseOrjsonModel | None:
                cache_key = self.get_cache_key(_method, *args, **kwargs)
                result = await self.get(cache_key, model_type)

                if result:
                    return result

                result = await method(*args, **kwargs)

                if result is not None:
                    await self.set(cache_key, result, ttl)

                return result

            return _method

        return _decorator
