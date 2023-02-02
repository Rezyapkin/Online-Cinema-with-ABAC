import orjson
from pydantic import parse_raw_as
from redis.asyncio import Redis, ConnectionError

from db.cache.base import BaseAsyncCacheStorage
from models.base import BaseOrjsonModel


class RedisAsyncCacheStorage(BaseAsyncCacheStorage):
    """Redis is a repository class of Pydantic models that uses or json for serialization/deserialization."""

    _storage: Redis

    def __init__(self, client: Redis):
        super().__init__(client)

    async def _ping(self) -> bool:
        result = True
        try:
            # ping is unsafe
            self._storage and await self._storage.ping()
        except ConnectionError:
            result = False

        return result

    async def set(self, key: str, value: BaseOrjsonModel, ttl: int) -> None:
        await self._storage.set(key, value.json(by_alias=True), ex=ttl)

    async def get(self, key: str, model_type: type[BaseOrjsonModel]) -> BaseOrjsonModel | None:
        value = await self._storage.get(key)

        if value is None:
            return None

        return parse_raw_as(model_type, value, json_loads=orjson.loads)
