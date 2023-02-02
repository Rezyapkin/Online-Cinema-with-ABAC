import pytest

from tests_src.test_data.models.auth import TokenResponse, ChangeEmailRequest
from tests_src.test_data.models.common import SuccessResponse
from tests_src.suites.base import BaseTestClass
from tests_src.clients.api_clients.grpc.utils import ErrorCode


class TestChangeEmail(BaseTestClass):
    async def _create_user_and_log_in(self, password: str, email: str | None = None) -> ChangeEmailRequest:
        creation_request = self.data_factory.generate_sign_up_request()
        if email:
            creation_request.email = email
        creation_request.password = password
        response = await self.grpc_client.user.create_user(creation_request)
        assert response.email == creation_request.email, "created user email must be the same as response email"

        login_request = self.data_factory.generate_log_in_request(
            email=creation_request.email, password=creation_request.password
        )
        token = await self.grpc_client.auth.log_in(login_request)
        assert isinstance(token, TokenResponse), "firs log_in must be successful"

        return ChangeEmailRequest(
            new_email=login_request.email,
            token=token.access_token,
            user_agent=login_request.user_agent,
            user_ip=login_request.ip,
        )

    async def test_change_email(self):
        """
        Check change email
        """
        password = self.utils.generate_string()
        email_req = await self._create_user_and_log_in(password)
        email_req.new_email = self.utils.generate_email()

        response = await self.grpc_client.auth.change_email(email_req)
        assert isinstance(response, SuccessResponse), "change email request must be successful"

        login_request = self.data_factory.generate_log_in_request(email=email_req.new_email, password=password)
        token = await self.grpc_client.auth.log_in(login_request)
        assert isinstance(token, TokenResponse), "log_in after email change must be successful"

    @pytest.mark.parametrize(
        "email",
        [
            "",
            "wrong_email_info",
            "@wrong_email_info",
            "wrong@email_info",
        ],
    )
    async def test_wrong_email(self, email):
        """
        Check errors by change email with wrong values.
        """
        password = self.utils.generate_string()
        email_req = await self._create_user_and_log_in(password)
        email_req.new_email = email

        response = await self.grpc_client.auth.change_email(email_req)

        assert response == ErrorCode.INVALID_ARGUMENT, "wrong parameter must occur corresponding error"

    async def test_old_email(self):
        """
        Check fail by log_in with old email.
        """
        old_email = self.utils.generate_email()
        password = self.utils.generate_string()
        email_req = await self._create_user_and_log_in(password=password, email=old_email)
        email_req.new_email = self.utils.generate_email()
        response = await self.grpc_client.auth.change_email(email_req)
        assert isinstance(response, SuccessResponse), "change email request must be successful"

        login_request = self.data_factory.generate_log_in_request(email=old_email, password=password)
        login_result = await self.grpc_client.auth.log_in(login_request)

        assert login_result == ErrorCode.NOT_FOUND, "wrong parameter must occur corresponding error"

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
    async def test_email_wrong_token(self, access_token: str, error: ErrorCode):
        """
        Check new user creation.
        """
        email = self.utils.generate_email()
        email_req = await self._create_user_and_log_in(email)
        email_req.new_email = self.utils.generate_email()
        email_req.token = access_token

        response = await self.grpc_client.auth.change_email(email_req)

        assert isinstance(response, ErrorCode)
        assert response == error
