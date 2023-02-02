from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, AsyncGenerator, Callable

import grpc

from middleware.signature_middleware import SignatureValidationInterceptor


class BaseController:
    def __init__(self, cache: Any, session_maker: Callable[[None], AsyncGenerator[AsyncSession, None]]):
        self.cache: Any = cache
        self.session_maker: Callable[[None], AsyncGenerator[AsyncSession, None]] = session_maker

    @staticmethod
    def get_user_agent(context: grpc.aio.ServicerContext) -> str:
        return [x for x in context.invocation_metadata() if x.key == SignatureValidationInterceptor.USER_AGENT][0].value

    @staticmethod
    def get_ip_address(context: grpc.aio.ServicerContext) -> str:
        return [x for x in context.invocation_metadata() if x.key == SignatureValidationInterceptor.IP_ADDRESS][0].value
