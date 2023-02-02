import time
from ipaddress import IPv4Address, ip_address
from typing import Callable, Coroutine

from faker import Faker
from loguru import logger

from tests_src.utils.exceptions import CustomDummyError, CustomTimeoutError

faker = Faker("en_US")


class Utils:
    @staticmethod
    async def wait(
        method: Callable[[], Coroutine],
        timeout: int | float = 5,
        interval: int | float = 0.1,
        err_msg: str = None,
        ignored_exceptions: type[BaseException] | list[type[BaseException]] = None,
    ):
        if ignored_exceptions is None:
            ignored_exceptions = CustomDummyError

        started = time.time()
        last_exception = None
        while (current_time := time.time() - started) < timeout:
            try:
                if outcome := await method():
                    logger.warning(
                        f"Success of Method {method.__name__} after: " f"{round(current_time, 3)}s from {timeout}"
                    )
                    return outcome
                last_exception = f"Method {method.__name__} returned {outcome}"
                time.sleep(interval)
            except ignored_exceptions as e:
                last_exception = e

        raise CustomTimeoutError(
            f"Method {method.__name__} timeout out in {timeout}sec with exception: {last_exception}\nerr_msg: {err_msg}"
        )

    @staticmethod
    def generate_string(length: int = 10) -> str:
        text = "?" * length
        return faker.lexify(text=text)

    @staticmethod
    def generate_email() -> str:
        return "{}@example.com".format(faker.lexify(text="?" * 10), faker.lexify(text="?" * 6))

    @staticmethod
    def generate_ip_v4() -> IPv4Address:
        return ip_address(".".join(str(faker.random.randint(0, 255)) for _ in range(4)))
