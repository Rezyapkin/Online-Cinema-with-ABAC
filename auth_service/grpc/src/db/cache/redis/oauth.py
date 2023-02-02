from uuid import uuid4

from db.cache.redis.redis import RedisAsyncCacheStorage
from models.base import BaseOrjsonModel


class StateInfo(BaseOrjsonModel):
    redirect_url: str
    user_id: str | None


class OAuthCacheStorage(RedisAsyncCacheStorage):
    """
    Storage for working with the state field of OAuth requests. As a state field, we form UUID-token, store it
    in the repository as a key and store information as a value that will be useful to us in subsequent requests.
    A unique state token protects against CSRF attacks and allows you to verify that the same state token is not used
    several times, or by different users.
    """

    STATE_TOKEN_KEY: str = "oauth_state_token:{}"
    TTL: int = 600  # Lifetime of the state token

    async def create_state_token(self, state_info: StateInfo) -> str:
        token = str(uuid4())
        await self.set(self.STATE_TOKEN_KEY.format(token), state_info, self.TTL)
        return token

    async def exist_state_token(self, token: str) -> bool:
        return bool(await self._storage.exists(self.STATE_TOKEN_KEY.format(token)))

    async def get_state_info(self, state_token: str) -> StateInfo | None:
        return await self.get(self.STATE_TOKEN_KEY.format(state_token), StateInfo)

    async def delete_state_token(self, state_token: str) -> None:
        await self._storage.delete(self.STATE_TOKEN_KEY.format(state_token))
