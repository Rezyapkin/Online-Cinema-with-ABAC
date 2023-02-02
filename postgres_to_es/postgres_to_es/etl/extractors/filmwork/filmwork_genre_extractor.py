from typing import Generator

from etl.extractors.filmwork.base_filmwork_extractor import BaseFilmworkExtractor
from models.updated_at_id import UpdatedAtId


class FilmworkGenreExtractor(BaseFilmworkExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.produce_table = "genre"

    def _produce(self) -> None:
        return super()._produce()

    @property
    def _enrich_query(self) -> str:
        return """
            SELECT DISTINCT
                fw.id, fw.updated_at
            FROM
                content.film_work fw
            LEFT JOIN
                content.genre_film_work gfw ON gfw.film_work_id = fw.id
            WHERE
                gfw.genre_id IN %s
            ORDER BY
                fw.updated_at;
        """

    def _enrich(self) -> Generator[None, tuple[str, list[UpdatedAtId]], None]:
        return super()._enrich()

    def _merge(self) -> Generator[None, tuple[str, list[UpdatedAtId]], None]:
        return super()._merge()
