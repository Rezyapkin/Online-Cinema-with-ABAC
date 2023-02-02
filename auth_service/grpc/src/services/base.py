from datetime import timedelta
from functools import wraps
from typing import Callable, Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pydantic import BaseModel
from pydantic.generics import GenericModel

from core.tracer import instrumented
from core.config import get_settings
from db.cache.redis.redis import RedisAsyncCacheStorage
from db.cache.redis.user import UserCacheStorage
from models.base import BaseOrjsonModel
from services.exceptions.exceptions import (
    AccessTokenBannedError,
    RefreshTokenUnknownError,
    TokenInvalidError,
    TokenExpiredError,
    TokenInvalidUserAgentError,
    AccessTokenCannotBeUsedAsRefreshTokenError,
    RefreshTokenCannotBeUsedAsAccessTokenError,
)
from services.helpers.jwt_token import JwtTokenService, JwtPayload, JwtTokenType


class BaseService:
    def __init__(self, cache: Any, session_maker: Callable[[], AsyncGenerator[AsyncSession, None]]):
        self.session_maker: Callable[[], AsyncGenerator[AsyncSession, None]] = session_maker
        self.cache_storage: RedisAsyncCacheStorage = RedisAsyncCacheStorage(client=cache)
        self.user_cache_manager: UserCacheStorage = UserCacheStorage(client=cache)
        self.default_cache_ttl: int = get_settings().default_cache_ttl

    @staticmethod
    def process_jwt(token: str, user_agent: str) -> JwtPayload:
        try:
            jwt_payload = JwtTokenService.decode_token(token=token)
        except ExpiredSignatureError:
            raise TokenExpiredError()
        except InvalidTokenError:
            raise TokenInvalidError()

        if user_agent != jwt_payload.user_agent:
            raise TokenInvalidUserAgentError()

        return jwt_payload

    @instrumented
    async def process_access_jwt(self, token: str, user_agent: str) -> JwtPayload:
        if await self.user_cache_manager.exists_access_token_in_blacklist(token):
            raise AccessTokenBannedError()
        jwt_payload = self.process_jwt(token=token, user_agent=user_agent)
        if jwt_payload.token_type != JwtTokenType.ACCESS:
            raise RefreshTokenCannotBeUsedAsAccessTokenError()

        return jwt_payload

    @instrumented
    async def process_refresh_jwt(self, token: str, user_agent: str) -> JwtPayload:
        jwt_payload = self.process_jwt(token=token, user_agent=user_agent)

        if jwt_payload.token_type != JwtTokenType.REFRESH:
            raise AccessTokenCannotBeUsedAsRefreshTokenError()

        # check that token belongs to UA and is latest generated for UA (suppose 1 device - 1 login)
        cached_user_refresh_token = await self.user_cache_manager.get_user_by_user_agent(
            user_id=jwt_payload.user,
            user_agent=jwt_payload.user_agent,
        )
        if token != cached_user_refresh_token:
            raise RefreshTokenUnknownError()

        return jwt_payload

    @staticmethod
    def cache(
        model_type: type[BaseModel | GenericModel | BaseOrjsonModel], ttl: timedelta | int | None = None
    ) -> Callable[[..., BaseModel | GenericModel | BaseOrjsonModel], Callable]:
        """Decorator for caching the values returned by the function, calling the decorator `cache_storage`."""

        def _decorator(method: Callable) -> Callable:
            @wraps(method)
            @instrumented
            async def _method(self, *args, **kwargs) -> BaseModel | GenericModel | BaseOrjsonModel:
                ttl_local = ttl

                if ttl_local is None:
                    ttl_local = self.default_cache_ttl

                return await self.cache_storage.cache_decorator(model_type, ttl_local)(method)(self, *args, **kwargs)

            return _method

        return _decorator
