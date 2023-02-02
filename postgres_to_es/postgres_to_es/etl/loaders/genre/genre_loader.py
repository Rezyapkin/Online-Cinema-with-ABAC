from datetime import datetime
from typing import Any, Generator

from etl.loaders.base_loader import BaseLoader
from helpers.logger import LoggerFactory
from models.genre import Genre

logger = LoggerFactory().get_logger()


class GenreLoader(BaseLoader):
    def _load(self, rows: list[Genre]) -> list[dict[str, Any]]:
        return [
            {
                "_op_type": "update",
                "_id": row.id,
                "doc": {
                    "id": row.id,
                    "name": row.name,
                },
                "doc_as_upsert": True,
                "retry_on_conflict": self.ELK_RETRY_ON_CONFLICT,
            }
            for row in rows
        ]

    def load(self) -> Generator[None, tuple[datetime, list[Genre]], None]:
        return super().load()
