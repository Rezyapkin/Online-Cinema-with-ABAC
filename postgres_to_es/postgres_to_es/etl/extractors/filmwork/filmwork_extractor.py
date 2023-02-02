from typing import Generator

from etl.extractors.filmwork.base_filmwork_extractor import BaseFilmworkExtractor
from models.updated_at_id import UpdatedAtId


class FilmworkExtractor(BaseFilmworkExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.produce_table = "film_work"

    def _produce(self) -> None:
        return super()._produce()

    @property
    def _enrich_query(self) -> str:
        raise NotImplementedError

    def _enrich(self) -> Generator[None, tuple[str, list[UpdatedAtId]], None]:
        """No need to enrich for filmwork"""
        pipe = self._merge()
        next(pipe)

        try:
            while True:
                last_updated, rows = yield
                pipe.send((last_updated, rows))

        except GeneratorExit:
            pass

    def _merge(self) -> Generator[None, tuple[str, list[UpdatedAtId]], None]:
        return super()._merge()
