import datetime
from abc import abstractmethod, ABC
from typing import Any, Generator

from helpers.logger import LoggerFactory
from helpers.state import State
from storage_clients.elasticsearch_client import ElasticsearchClient

logger = LoggerFactory().get_logger()


class BaseLoader(ABC):
    ELK_RETRY_ON_CONFLICT = 5

    def __init__(
        self,
        elk_conn: ElasticsearchClient,
        state: State,
        elk_index: str,
        load_chunk: int,
    ):
        self.elk_conn = elk_conn
        self.state = state
        self.elk_index = elk_index
        self.load_chunk = load_chunk

    def __repr__(self):
        return f"{self.__class__.__name__} for state: {self.state.key}"

    @abstractmethod
    def _load(self, rows: list[Any]) -> list[dict[str, Any]]:
        """Method to prepare and load data, based on ELK index."""
        raise NotImplementedError

    @abstractmethod
    def load(self) -> Generator[None, tuple[datetime.datetime, list[Any]], None]:
        """Method to load data to ELK. Send data to loader. Receive data from transformer."""
        saved_state = None

        try:
            while True:
                last_updated, rows = yield
                data = self._load(rows)

                self.elk_conn.bulk(
                    actions=data,
                    chunk_size=self.load_chunk,
                    index=self.elk_index,
                )

                if not saved_state:
                    saved_state = last_updated
                elif saved_state != last_updated:
                    # save index on each cycle of fetchmany in produce
                    logger.warn(
                        "Extract cycle finished, updating index: `%s` with value: `%s`", self.state.key, saved_state
                    )
                    self.state.set(str(saved_state))
                    saved_state = last_updated

        except GeneratorExit:
            logger.debug("Load loop finished: `%r`", self)
            if saved_state:
                logger.warn("Updating index: `%s` with value: `%s`", self.state.key, saved_state)
                self.state.set(str(saved_state))
