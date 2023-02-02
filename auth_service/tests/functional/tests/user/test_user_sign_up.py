import pytest

from tests_src.suites.base import BaseTestClass
from tests_src.test_data.models.user import SignUpResponse
from tests_src.clients.api_clients.grpc.utils import ErrorCode


class TestSignUp(BaseTestClass):
    async def test_sign_up(self):
        """
        Check new user creation.
        """
        request = self.data_factory.generate_sign_up_request()

        response = await self.grpc_client.user.create_user(request)

        assert isinstance(response, SignUpResponse)
        assert response.email == request.email

    async def test_duplicate_sign_up(self):
        """
        The same account mustn't be created
        """
        request = self.data_factory.generate_sign_up_request()

        response = await self.grpc_client.user.create_user(request)
        failed_response = await self.grpc_client.user.create_user(request)

        assert isinstance(response, SignUpResponse)
        assert response.email == request.email
        assert failed_response == ErrorCode.ALREADY_EXISTS

    @pytest.mark.parametrize(
        "email, password",
        [
            ("", "123"),
            ("wrong_email", "123"),
            ("@wrong_email_info", "123"),
            ("wrong@email_info", "123"),
            ("wrong@@email.info", "123"),
            ("a@b.com", ""),
            ("", ""),
        ],
    )
    async def test_wrong_parameters(self, email, password):
        """
        User creation with wrong parameters must be failed
        """
        request = self.data_factory.generate_sign_up_request()
        request.email = email
        request.password = password

        failed_response = await self.grpc_client.user.create_user(request)

        assert failed_response == ErrorCode.INVALID_ARGUMENT
