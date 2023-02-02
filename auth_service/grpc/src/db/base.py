import time
from abc import ABC, abstractmethod
from typing import TypeVar, Any, Generic

from models.postgres import SchemaInDbType

BaseCrudModelType = TypeVar("BaseCrudModelType", bound=Any)


class AbstractAsyncStorage(ABC):
    def __init__(self, client: Any):
        self._storage: Any = client

    async def ping(self) -> tuple[bool, str]:
        """
        An abstract method to check the storage state
        """
        started_at = time.time()
        result = await self._ping()
        diff = str(time.time() - started_at)
        return result, diff

    @abstractmethod
    async def _ping(self) -> bool:
        """
        An abstract method to check the storage state
        """
        raise NotImplementedError

    async def close_storage(self) -> None:
        await self._storage.close()


class AbstractAsyncCrudStorage(AbstractAsyncStorage, ABC, Generic[SchemaInDbType, BaseCrudModelType]):
    @abstractmethod
    async def get(self, *args, **kwargs) -> BaseCrudModelType:
        raise NotImplementedError

    @abstractmethod
    async def get_multi(self, *args, **kwargs) -> list[BaseCrudModelType]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs) -> BaseCrudModelType | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, *args, **kwargs) -> BaseCrudModelType | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs) -> BaseCrudModelType | None:
        raise NotImplementedError
