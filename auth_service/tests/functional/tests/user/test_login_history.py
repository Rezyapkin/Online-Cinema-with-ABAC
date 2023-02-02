import pytest

from tests_src.test_data.models.auth import TokenResponse
from tests_src.test_data.models.user import LogInHistory, LogInHistoryResponse
from tests_src.test_data.models.common import CommonRequest, ExpectedPagination
from tests_src.clients.api_clients.grpc.utils import ErrorCode
from tests_src.suites.base import BaseTestClass

_CHECKED_ENTRIES = 5
_PAGE_ZERO_SIZE_VALUE = 10


class TestLogInHistory(BaseTestClass):
    async def _login_x_times(self, x: int) -> CommonRequest:
        creation_request = self.data_factory.generate_sign_up_request()
        creation_response = await self.grpc_client.user.create_user(creation_request)
        assert (
            creation_response.email == creation_request.email
        ), "created user email must be the same as response email"
        login_request = self.data_factory.generate_log_in_request(
            email=creation_request.email, password=creation_request.password
        )

        output = None
        for i in range(x):
            token = await self.grpc_client.auth.log_in(login_request)
            assert isinstance(token, TokenResponse), "Correct 'log_in' must contain Token"

            output = CommonRequest(
                token=token.access_token, user_agent=login_request.user_agent, user_ip=login_request.ip
            )
            if i + 1 < x:
                await self.grpc_client.auth.log_out(output)

        return output

    def _assert_pagination(self, response: LogInHistoryResponse, expected: ExpectedPagination):
        assert isinstance(response, LogInHistoryResponse), "log_in_history response must be a list"
        if len(response.data):
            assert isinstance(
                response.data[0], LogInHistory
            ), "log_in_history response with data must contain a list of 'LogInHistoryResponse'"
        assert (
            len(response.data) == expected.data_size
        ), "log_in_history response elements count must depends on page_size and page_number"
        assert (
            response.next_page == expected.next_page
        ), "log_in_history response next_page must be the same as expected"
        assert (
            response.prev_page == expected.prev_page
        ), "log_in_history response next_page must be the same as expected"

    @pytest.mark.parametrize("page_number, page_size", [(1, 1), (2, 3), (1, 0), (1, 1_000_000)])
    async def test_history_pagination(self, page_number: int, page_size: int):
        """
        Check log in history
        """
        cmn_request = await self._login_x_times(_CHECKED_ENTRIES)
        history_request = self.data_factory.generate_log_in_history_request(
            page_number=page_number, page_size=page_size, common=cmn_request
        )
        expected = self.data_factory.get_expected_pagination(
            page_size=page_size,
            page_number=page_number,
            page_zero_size_value=_PAGE_ZERO_SIZE_VALUE,
            total_elements=_CHECKED_ENTRIES,
        )

        response = await self.grpc_client.user.get_log_in_history(history_request)

        self._assert_pagination(response=response, expected=expected)

    @pytest.mark.parametrize(
        "page_number, page_size, error_code",
        [
            # protocol doesn't support negative values
            (-1, 1, ErrorCode.INTERNAL_ERROR),
            (1, -1, ErrorCode.INTERNAL_ERROR),
            (-1, -1, ErrorCode.INTERNAL_ERROR),
            # logical wrong values
            (0, 1, ErrorCode.INVALID_ARGUMENT),
            (1_00_000, 1, ErrorCode.NOT_FOUND),
        ],
    )
    async def test_history_wrong_pagination(self, page_number: int, page_size: int, error_code: ErrorCode | None):
        """
        Check wrong parameters for log in_history
        """
        cmn_request = await self._login_x_times(_CHECKED_ENTRIES)

        history_request = self.data_factory.generate_log_in_history_request(
            page_number=page_number, page_size=page_size, common=cmn_request
        )
        response = await self.grpc_client.user.get_log_in_history(history_request)

        if error_code:
            assert response == error_code
        else:
            expected = self.data_factory.get_expected_pagination(
                page_size=page_size,
                page_number=page_number,
                page_zero_size_value=_PAGE_ZERO_SIZE_VALUE,
                total_elements=_CHECKED_ENTRIES,
            )
            self._assert_pagination(response=response, expected=expected)

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
        cmn_request = await self._login_x_times(1)
        cmn_request.token = access_token

        history_request = self.data_factory.generate_log_in_history_request(
            page_size=0, page_number=_CHECKED_ENTRIES, common=cmn_request
        )
        response = await self.grpc_client.user.get_log_in_history(history_request)

        assert response == error, "errors should be as expected"
