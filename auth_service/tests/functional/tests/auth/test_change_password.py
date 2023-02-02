import pytest

from tests_src.test_data.models.auth import TokenResponse, ChangePasswordRequest
from tests_src.test_data.models.common import SuccessResponse
from tests_src.suites.base import BaseTestClass
from tests_src.clients.api_clients.grpc.utils import ErrorCode


class TestChangePassword(BaseTestClass):
    async def _create_user_and_log_in(self, email: str, password: str | None = None) -> ChangePasswordRequest:
        creation_request = self.data_factory.generate_sign_up_request()
        creation_request.email = email
        if password:
            creation_request.password = password
        creation_response = await self.grpc_client.user.create_user(creation_request)
        assert (
            creation_response.email == creation_request.email
        ), "created user email must be the same as response email"

        login_request = self.data_factory.generate_log_in_request(
            email=creation_request.email, password=creation_request.password
        )
        token = await self.grpc_client.auth.log_in(login_request)
        assert isinstance(token, TokenResponse), "firs log_in must be successful"

        return ChangePasswordRequest(
            new_password=login_request.password,
            token=token.access_token,
            user_agent=login_request.user_agent,
            user_ip=login_request.ip,
        )

    async def test_change_password(self):
        """
        Check password change
        """
        email = self.utils.generate_email()
        password_req = await self._create_user_and_log_in(email)
        password_req.new_password = self.utils.generate_string()

        response = await self.grpc_client.auth.change_password(password_req)
        assert isinstance(response, SuccessResponse), "change password request must be successful"

        login_request = self.data_factory.generate_log_in_request(email=email, password=password_req.new_password)
        token = await self.grpc_client.auth.log_in(login_request)
        assert isinstance(token, TokenResponse), "log_in after password change must be successful"

    @pytest.mark.parametrize("password", [""])
    async def test_wrong_password(self, password):
        """
        Check errors by change password with wrong values.
        """
        email = self.utils.generate_email()
        password_req = await self._create_user_and_log_in(email)
        password_req.new_password = password

        response = await self.grpc_client.auth.change_password(password_req)

        assert response == ErrorCode.INVALID_ARGUMENT, "wrong parameter must occur corresponding error"

    async def test_old_password(self):
        """
        Check fail by log_in with old password.
        """
        email = self.utils.generate_email()
        password_req = await self._create_user_and_log_in(email)
        old_password = password_req.new_password
        password_req.new_password = self.utils.generate_string()
        password_response = await self.grpc_client.auth.change_password(password_req)
        assert isinstance(password_response, SuccessResponse), "change password request must be successful"
        login_request = self.data_factory.generate_log_in_request(email=email, password=password_req.new_password)
        login_request.password = old_password

        password_response = await self.grpc_client.auth.log_in(login_request)

        assert password_response == ErrorCode.UNAUTHENTICATED, "wrong parameter must occur corresponding error"

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
    async def test_password_wrong_token(self, access_token: str, error: ErrorCode):
        """
        Check change password with wrong access token
        """
        email = self.utils.generate_email()
        password_req = await self._create_user_and_log_in(email)
        password_req.new_password = self.utils.generate_string()
        password_req.token = access_token

        response = await self.grpc_client.auth.change_password(password_req)

        assert response == error, "wrong parameter must occur corresponding error"
