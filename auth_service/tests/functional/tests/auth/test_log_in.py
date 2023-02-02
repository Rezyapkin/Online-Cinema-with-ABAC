from tests_src.test_data.models.auth import TokenResponse
from tests_src.test_data.models.user import SignUpRequest
from tests_src.suites.base import BaseTestClass
from tests_src.clients.api_clients.grpc.utils import ErrorCode


class TestLogIn(BaseTestClass):
    async def _create_user(self) -> SignUpRequest:
        creation_request = self.data_factory.generate_sign_up_request()
        creation_response = await self.grpc_client.user.create_user(creation_request)
        assert (
            creation_response.email == creation_request.email
        ), "created user email must be the same as response email"
        return creation_request

    async def test_double_access(self):
        """
        Try to obtain some tokens y double access
        """
        creation_request = await self._create_user()
        login_request = self.data_factory.generate_log_in_request(
            email=creation_request.email, password=creation_request.password
        )

        first_response = await self.grpc_client.auth.log_in(login_request)

        second_response = await self.grpc_client.auth.log_in(login_request)

        assert isinstance(first_response, TokenResponse)
        assert isinstance(second_response, TokenResponse)

    async def test_wrong_password(self):
        """
        Check errors by wrong password.
        """
        creation_request = await self._create_user()
        creation_request.password = self.utils.generate_string()
        login_request = self.data_factory.generate_log_in_request(
            email=creation_request.email, password=creation_request.password
        )

        response = await self.grpc_client.auth.log_in(login_request)

        assert response == ErrorCode.UNAUTHENTICATED, "wrong parameter must occur corresponding error"

    async def test_missed_account(self):
        """
        Check errors by wrong email.
        """
        creation_request = await self._create_user()
        creation_request.password = self.utils.generate_email()
        login_request = self.data_factory.generate_log_in_request(
            email=creation_request.email, password=creation_request.password
        )

        response = await self.grpc_client.auth.log_in(login_request)

        assert response == ErrorCode.UNAUTHENTICATED, "wrong parameter must occur corresponding error"
