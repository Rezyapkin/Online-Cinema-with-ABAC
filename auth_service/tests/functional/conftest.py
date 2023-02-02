import asyncio
import sys
from asyncio import AbstractEventLoop

import pytest
from loguru import logger

pytest_plugins = ("tests_src.fixtures.grpc", "tests_src.fixtures.settings", "tests_src.fixtures.check_backend_is_up")


def pytest_addoption(parser):
    parser.addoption("--log_level", help="Уровень логирования", default="INFO")


def pytest_configure(config):
    # Создаем главного логера
    logger.remove()
    log_format = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {file}:{function}:{line} | {message}"
    log_level = config.getoption("--log_level")
    logger.add(sys.stderr, level=log_level, format=log_format, enqueue=True)
    logger.info("pytest_configure started..")


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    try:
        e_loop = asyncio.get_running_loop()
    except RuntimeError:
        e_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(e_loop)

    yield e_loop
