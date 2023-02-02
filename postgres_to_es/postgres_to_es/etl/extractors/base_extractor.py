import datetime
from abc import ABC, abstractmethod
from typing import Callable, Generator, Any

from helpers.logger import LoggerFactory
from helpers.state import State
from storage_clients.postgres_client import PostgresClient

logger = LoggerFactory().get_logger()


class BaseExtractor(ABC):
    def __init__(
        self,
        pg_conn: PostgresClient,
        state: State,
        extract_chunk: int,
        transform_pipe: Callable[[], Generator[None, tuple[datetime.datetime, list[Any]] | None, None]],
    ):
        self.state = state
        self.pg_conn = pg_conn
        self.extract_chunk = extract_chunk
        self.transform_pipe = transform_pipe

    def __repr__(self):
        return f"{self.__class__.__name__} for state: {self.state.key}"

    @abstractmethod
    def extract(self) -> None:
        """Start pipeline: [extract [-> transform -> [load]]], where [] mean inner loops."""
        raise NotImplementedError
