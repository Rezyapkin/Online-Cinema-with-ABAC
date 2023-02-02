import argparse
import asyncio
from asyncio import CancelledError

import grpc
import uvloop
from loguru import logger
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import db.cache
import db.storage
from api.grpc.admin_role import AdminRoleController
from api.grpc.auth import AuthController
from api.grpc.user import UserController
from api.grpc.oauth.google import GoogleOAuthController
from api.grpc.oauth.yandex import YandexOAuthController
from core.config import get_settings
from grpc_auth_service import (
    auth_service_pb2_grpc,
    user_service_pb2_grpc,
    role_service_pb2_grpc,
    oauth_service_pb2_grpc,
)
from core.logger import setup_logger
from core.tracer import setup_tracer
from middleware.exception_to_status_middleware import ExceptionToStatusMiddleware
from middleware.logger_middleware import LoggerInterceptor
from middleware.signature_middleware import SignatureValidationInterceptor
from services.helpers.http_client import close_all_http_clients

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", nargs="?", type=int, default=50051, help="The serving port")
    return parser.parse_args()


def on_startup() -> None:
    setup_logger()
    # init redis
    db.cache.cache = aioredis.from_url(get_settings().redis_dsn, encoding="utf-8", decode_responses=True)
    # init RSQL engine
    db.storage.engine = create_async_engine(get_settings().postgres_dsn, echo=True, future=True)
    db.storage.session_maker = sessionmaker(db.storage.engine, class_=AsyncSession, expire_on_commit=False)


async def on_shutdown() -> None:
    await db.cache.cache.close()
    await db.storage.engine.dispose()
    await close_all_http_clients()


async def serve(arguments: argparse.Namespace):
    on_startup()

    try:
        interceptors = [ExceptionToStatusMiddleware(), SignatureValidationInterceptor(), LoggerInterceptor()]

        if not get_settings().testing:
            interceptors.insert(0, setup_tracer())

        server = grpc.aio.server(interceptors=interceptors)
        auth_service_pb2_grpc.add_AuthServicer_to_server(
            AuthController(cache=db.cache.get_cache(), session_maker=db.storage.get_session),
            server,
        )
        user_service_pb2_grpc.add_UserServicer_to_server(
            UserController(cache=db.cache.get_cache(), session_maker=db.storage.get_session),
            server,
        )
        role_service_pb2_grpc.add_AdminRoleServicer_to_server(
            AdminRoleController(cache=db.cache.get_cache(), session_maker=db.storage.get_session),
            server,
        )
        oauth_service_pb2_grpc.add_GoogleOAuthServicer_to_server(
            GoogleOAuthController(cache=db.cache.get_cache(), session_maker=db.storage.get_session),
            server,
        )
        oauth_service_pb2_grpc.add_YandexOAuthServicer_to_server(
            YandexOAuthController(cache=db.cache.get_cache(), session_maker=db.storage.get_session),
            server,
        )
        listen_addr = f"[::]:{arguments.port}"
        server.add_insecure_port(listen_addr)
        logger.info("Starting server on {}", listen_addr)
        await server.start()
        await server.wait_for_termination()
    except CancelledError:
        logger.warning("Shutting down server on event loop cancel")
    finally:
        await on_shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(serve(arguments=get_args()))
    except KeyboardInterrupt:
        logger.warning("KeyboardInterrupt")
