from datetime import datetime
from typing import Generator

from etl.transformers.base_transformer import BaseTransformer
from helpers.logger import LoggerFactory
from models.genre import Genre

logger = LoggerFactory().get_logger()


class GenreTransformer(BaseTransformer):
    def _transform(self, rows: list[Genre]) -> None:
        """Method to transform data, based on model."""
        return super()._transform(rows)

    def transform(self) -> Generator[None, tuple[datetime, list[Genre]], None]:
        """Method to transform data. Send data to loader. Receive data from merger."""
        return super().transform()
