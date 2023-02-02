from typing import Generator

from etl.transformers.base_transformer import BaseTransformer
from helpers.logger import LoggerFactory
from models.filmwork import Filmwork

logger = LoggerFactory().get_logger()


class FilmworkTransformer(BaseTransformer):
    def _transform(self, rows: list[Filmwork]) -> None:
        """Method to transform data, based on model."""
        return super()._transform(rows)

    def transform(self) -> Generator[None, tuple[str, list[Filmwork]], None]:
        """Method to transform data. Send data to loader. Receive data from merger."""
        return super().transform()
