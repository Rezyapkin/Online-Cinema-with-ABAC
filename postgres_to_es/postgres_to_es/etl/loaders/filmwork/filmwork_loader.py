import datetime
from typing import Any, Generator

from etl.loaders.base_loader import BaseLoader
from helpers.logger import LoggerFactory
from models.filmwork import Filmwork

logger = LoggerFactory().get_logger()


class FilmworkLoader(BaseLoader):
    def _load(self, rows: list[Filmwork]) -> list[dict[str, Any]]:
        return [
            {
                "_op_type": "update",
                "_id": row.id,
                "doc": {
                    "id": row.id,
                    "imdb_rating": row.rating,
                    "title": row.title,
                    "description": row.description,
                    "filmwork_type": row.type,
                    "release_date": row.creation_date,
                    "file_path": row.file_path,
                    "age_limit": row.age_limit,
                    "genres_names": row.genres_names,
                    "genres": [dict(genre) for genre in row.genres],
                    "directors_names": row.directors_names,
                    "actors_names": row.actors_names,
                    "writers_names": row.writers_names,
                    "directors": [dict(director) for director in row.directors],
                    "actors": [dict(actor) for actor in row.actors],
                    "writers": [dict(writer) for writer in row.writers],
                },
                "doc_as_upsert": True,
                "retry_on_conflict": self.ELK_RETRY_ON_CONFLICT,
            }
            for row in rows
        ]

    def load(self) -> Generator[None, tuple[datetime.datetime, list[Filmwork]], None]:
        return super().load()
