from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable, Generator, Any

from helpers.logger import LoggerFactory

logger = LoggerFactory().get_logger()


class BaseTransformer(ABC):
    def __init__(
        self,
        load_pipe: Callable[[], Generator[None, tuple[datetime, list[Any]] | None, None]],
    ):
        self.load_pipe = load_pipe

    def __repr__(self):
        return f"{self.__class__.__name__}"

    @abstractmethod
    def _transform(self, rows: list[Any]) -> None:
        """Method to transform data, based on model."""
        for row in rows:
            row.transform()

    @abstractmethod
    def transform(self) -> Generator[None, tuple[datetime, list[Any]], None]:
        """Method to transform data. Send data to loader. Receive data from merger."""
        pipe = self.load_pipe()
        next(pipe)

        try:
            while True:
                last_updated, rows = yield
                self._transform(rows)

                pipe.send((last_updated, rows))
        except GeneratorExit:
            logger.debug("Transform loop finished: `%r`.", self)
