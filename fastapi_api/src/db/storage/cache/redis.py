import orjson
from pydantic import parse_raw_as
from redis.asyncio import Redis, ConnectionError

from core.helpers.utils import orjson_dumps
from db.storage.cache.base import AbstractAsyncCacheStorage, IndexModelType


class RedisAsyncCacheStorage(AbstractAsyncCacheStorage):
    """Redis is a repository class of Pydantic models that uses or json for serialization/deserialization."""

    def __init__(self, client: Redis):
        self._storage: Redis
        super().__init__(client)

    async def ping(self) -> bool:
        result = True
        try:
            # ping is unsafe
            self._storage and await self._storage.ping()
        except ConnectionError:
            result = False

        return result

    async def set(self, key: str, value: IndexModelType, ttl: int):
        await self._storage.set(key, value.json(encoder=orjson_dumps, by_alias=True), ex=ttl)

    async def get(self, key: str, model_type: type[IndexModelType]) -> IndexModelType | None:
        value = await self._storage.get(key)

        if value is None:
            return None

        return parse_raw_as(model_type, value, json_loads=orjson.loads)
