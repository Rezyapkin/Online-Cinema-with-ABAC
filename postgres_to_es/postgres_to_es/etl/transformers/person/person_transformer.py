from datetime import datetime
from typing import Generator

from etl.transformers.base_transformer import BaseTransformer
from helpers.logger import LoggerFactory
from models.person import Person

logger = LoggerFactory().get_logger()


class PersonTransformer(BaseTransformer):
    def _transform(self, rows: list[Person]) -> None:
        """Method to transform data, based on model."""
        return super()._transform(rows)

    def transform(self) -> Generator[None, tuple[datetime, list[Person]], None]:
        """Method to transform data. Send data to loader. Receive data from merger."""
        return super().transform()
