from functools import lru_cache

from redis.asyncio import Redis

cache: Redis | None = None


@lru_cache
def get_cache() -> Redis:
    """Cache Storage Provider."""
    return cache
