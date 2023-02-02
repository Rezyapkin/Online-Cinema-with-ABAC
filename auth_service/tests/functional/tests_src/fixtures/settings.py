import pytest

from settings import Settings


@pytest.fixture(scope="session", autouse=True)
def settings() -> Settings:
    settings = Settings()
    return settings
