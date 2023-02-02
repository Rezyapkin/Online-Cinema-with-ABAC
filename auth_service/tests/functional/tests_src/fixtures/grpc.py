from typing import AsyncGenerator

import pytest_asyncio

from settings import Settings
from tests_src.clients.api_clients.grpc.base import GrpcChannel
from tests_src.clients.api_clients.grpc.client import GrpcClient


@pytest_asyncio.fixture(scope="session")
async def grpc_client(grpc_channel: GrpcChannel) -> AsyncGenerator[GrpcClient, None]:
    client = GrpcClient(grpc_channel)

    yield client


@pytest_asyncio.fixture(scope="session")
async def grpc_channel(settings: Settings) -> AsyncGenerator[GrpcChannel, None]:
    client = GrpcChannel(settings.grpc_dsn)

    yield client
