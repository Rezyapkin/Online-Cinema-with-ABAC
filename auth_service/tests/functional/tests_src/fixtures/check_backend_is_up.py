import pytest_asyncio

from tests_src.clients.api_clients.grpc.client import GrpcClient
from tests_src.utils.utils import Utils


@pytest_asyncio.fixture(scope="session", autouse=True)
async def check_backend_is_up(grpc_client: GrpcClient) -> None:
    await Utils.wait(grpc_client.auth.ping, interval=1, timeout=5, err_msg="GRPC server is not ready...")
