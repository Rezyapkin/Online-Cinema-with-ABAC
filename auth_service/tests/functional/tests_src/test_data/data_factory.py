from tests_src.test_data.models.common import CommonRequest, ExpectedPagination
from tests_src.utils.utils import Utils
from tests_src.test_data.models.user import SignUpRequest, LogInHistoryRequest
from tests_src.test_data.models.auth import LogInRequest


class DataFactory:
    @staticmethod
    def generate_sign_up_request() -> SignUpRequest:
        return SignUpRequest(
            email=Utils.generate_email(),
            password=Utils.generate_string(),
            user_agent=Utils.generate_string(15),
            ip=Utils.generate_ip_v4(),
        )

    @staticmethod
    def generate_log_in_request(email: str, password: str) -> LogInRequest:
        return LogInRequest(
            email=email,
            password=password,
            user_agent=Utils.generate_string(15),
            ip=Utils.generate_ip_v4(),
        )

    @staticmethod
    def generate_log_in_history_request(page_number: int, page_size: int, common: CommonRequest) -> LogInHistoryRequest:
        return LogInHistoryRequest(
            page_number=page_number,
            page_size=page_size,
            user_agent=common.user_agent,
            user_ip=common.user_ip,
            token=common.token,
        )

    @staticmethod
    def generate_common_request_from_log_in(access_token: str, log_in: LogInRequest) -> CommonRequest:
        return CommonRequest(
            user_agent=log_in.user_agent,
            user_ip=log_in.ip,
            token=access_token,
        )

    @staticmethod
    def get_expected_pagination(
        page_size: int, page_number: int, page_zero_size_value: int, total_elements: int
    ) -> ExpectedPagination:
        page_size = page_size if page_size else page_zero_size_value
        page_size = page_size if page_size < total_elements else total_elements
        offset = page_size * (page_number - 1)

        count = total_elements - offset
        if count > page_size:
            count = page_size
        elif count < 0:
            count = 0

        prev_page = page_number - 1
        if prev_page <= 0:
            prev_page = None
        elif (offset - page_size) > total_elements:
            prev_page = None

        # count = page_size if (count := total_elements - offset) > page_size else count
        next_page = page_number + 1 if (offset + page_size) < total_elements else None
        # prev_page = page_number - 1 if (offset - page_size) >= 0 else None

        return ExpectedPagination(data_size=count, prev_page=prev_page, next_page=next_page)
