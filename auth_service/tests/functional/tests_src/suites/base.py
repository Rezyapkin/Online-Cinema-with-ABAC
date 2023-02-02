import pytest

from tests_src.clients.api_clients.grpc.client import GrpcClient

from tests_src.test_data.data_factory import DataFactory
from tests_src.utils.utils import Utils


# noinspection PyAttributeOutsideInit
# noinspection PyUnusedLocal
class BaseTestClass:
    @pytest.fixture(autouse=True)
    def prepare(
        self,
        check_backend_is_up,
        grpc_client: GrpcClient,
    ):
        self.utils: Utils = Utils()
        self.grpc_client = grpc_client
        self.data_factory: DataFactory = DataFactory()
