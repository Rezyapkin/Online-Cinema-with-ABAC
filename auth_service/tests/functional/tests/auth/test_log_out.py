import pytest

from tests_src.test_data.models.auth import TokenResponse
from tests_src.test_data.models.common import SuccessResponse
from tests_src.test_data.models.common import CommonRequest
from tests_src.clients.api_clients.grpc.utils import ErrorCode
from tests_src.suites.base import BaseTestClass


class TestLogOutHistory(BaseTestClass):
    async def _login(self) -> CommonRequest:
        creation_request = self.data_factory.generate_sign_up_request()
        creation_response = await self.grpc_client.user.create_user(creation_request)
        assert (
            creation_response.email == creation_request.email
        ), "created user email must be the same as response email"
        login_request = self.data_factory.generate_log_in_request(
            email=creation_request.email, password=creation_request.password
        )

        token = await self.grpc_client.auth.log_in(login_request)
        assert isinstance(token, TokenResponse), "Correct 'log_in' must contain Token"

        return CommonRequest(token=token.access_token, user_agent=login_request.user_agent, user_ip=login_request.ip)

    async def test_double_out(self):
        """
        Try to log out twice and get the error
        """
        common_request = await self._login()

        first_response = await self.grpc_client.auth.log_out(common_request)

        second_response = await self.grpc_client.auth.log_out(common_request)

        assert isinstance(first_response, SuccessResponse)
        assert second_response == ErrorCode.UNAUTHENTICATED

    @pytest.mark.parametrize(
        "access_token, error",
        [
            ("", ErrorCode.INVALID_ARGUMENT),
            (
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0Ijo\
                xNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
                ErrorCode.UNAUTHENTICATED,
            ),
        ],
    )
    async def test_history_wrong_token(self, access_token: str, error: ErrorCode):
        """
        Check log in history request with wrong access token
        """
        cmn_request = await self._login()
        cmn_request.token = access_token

        response = await self.grpc_client.auth.log_out(cmn_request)

        assert response == error, "errors should be as expected"
