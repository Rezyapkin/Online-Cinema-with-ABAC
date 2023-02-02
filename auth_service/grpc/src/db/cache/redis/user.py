from datetime import timedelta

from db.cache.redis.redis import RedisAsyncCacheStorage


class UserCacheStorage(RedisAsyncCacheStorage):
    BLACKLIST_KEY: str = "blacklist:{}"
    USER_KEY: str = "user:{}"

    async def add_access_token_to_blacklist(self, access_token: str, expires_in: int | timedelta) -> None:
        """Добавление access токена в блэклист."""
        await self._storage.setex(name=self.BLACKLIST_KEY.format(access_token), time=expires_in, value="true")

    async def exists_access_token_in_blacklist(self, access_token: str) -> bool:
        """Поиск access токена в блэклисте."""
        return bool(await self._storage.exists(self.BLACKLIST_KEY.format(access_token)))

    async def add_user(self, user_id: str, user_agent: str, refresh_token: str, expires_in: int | timedelta) -> None:
        """Сохраняем в редисе информацию о юзере: маппинг UA на refresh токен."""
        await self._storage.hset(name=self.USER_KEY.format(user_id), key=user_agent, value=refresh_token)
        await self._storage.expire(name=self.USER_KEY.format(user_id), time=expires_in)

    async def get_user(self, user_id: str) -> dict[str, str]:
        """Получение всех refresh токенов юзера."""
        return await self._storage.hgetall(name=self.USER_KEY.format(user_id))

    async def get_user_by_user_agent(self, user_id: str, user_agent: str) -> str:
        """Получение refresh токена юзера по user_agent."""
        return await self._storage.hget(name=self.USER_KEY.format(user_id), key=user_agent)

    async def delete_user(self, user_id: str) -> None:
        """Удаление всех refresh токенов юзера."""
        await self._storage.delete(self.USER_KEY.format(user_id))

    async def delete_user_by_user_agent(self, user_id: str, user_agent: str) -> None:
        """Удаление refresh токена юзера по user_agent"""
        await self._storage.hdel(self.USER_KEY.format(user_id), user_agent)
