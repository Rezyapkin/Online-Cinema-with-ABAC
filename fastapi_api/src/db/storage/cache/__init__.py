from fastapi import Request

from functools import lru_cache

from db.storage.cache.base import AbstractAsyncCacheStorage


@lru_cache
def get_cache_storage(request: Request) -> AbstractAsyncCacheStorage:
    """Get Cache Storage base Adapter."""
    return request.app.state.cache
