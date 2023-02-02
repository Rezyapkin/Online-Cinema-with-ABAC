from abc import ABC, abstractmethod
from typing import Generator

from psycopg2.sql import SQL, Identifier

from etl.extractors.base_extractor import BaseExtractor
from helpers.logger import LoggerFactory
from models.filmwork import Filmwork
from models.updated_at_id import UpdatedAtId

logger = LoggerFactory().get_logger()


class BaseFilmworkExtractor(BaseExtractor, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.produce_table: str | None = None

    def extract(self) -> None:
        """Start pipeline: [produce [-> merge [-> enrich [-> transform -> [load]]]]], where [] mean inner loops."""
        self._produce()

    @abstractmethod
    def _produce(self) -> None:
        """Method to monitor data update in PGSQL. Send data to enricher."""
        started = False

        with self.pg_conn.cursor() as cur:
            cur.execute(
                SQL(
                    """
                    SELECT
                        id, updated_at
                    FROM
                        content.{produce_table}
                    WHERE
                        updated_at > %s
                    ORDER BY
                        updated_at;
                """
                ).format(produce_table=Identifier(self.produce_table)),
                [self.state.get().updated_at],
            )
            while results := cur.fetchmany(self.extract_chunk):
                if not started:
                    # not to generate extra cursors
                    pipe = self._enrich()
                    next(pipe)
                    started = True

                data = [UpdatedAtId(**result) for result in results]
                last_updated = data[-1].updated_at
                pipe.send((last_updated, data))

            logger.info("Extract loop finished: `%r`. Going to start a new loop.", self)

    @property
    @abstractmethod
    def _enrich_query(self) -> SQL | str:
        raise NotImplementedError

    @abstractmethod
    def _enrich(self) -> Generator[None, tuple[str, list[UpdatedAtId]], None]:
        """Method to enrich data. Send data to merger. Receive data from producer"""
        started = False

        with self.pg_conn.cursor() as cur:
            try:
                while True:
                    last_updated, rows = yield
                    rows: list[UpdatedAtId]

                    cur.execute(
                        self._enrich_query,
                        [tuple([row.id for row in rows])],  # psycopg2 is awesome ;<)
                    )

                    while results := cur.fetchmany(self.extract_chunk):
                        if not started:
                            # not to generate extra cursors
                            pipe = self._merge()
                            next(pipe)
                            started = True

                        pipe.send((last_updated, [UpdatedAtId(**result) for result in results]))
            except GeneratorExit:
                logger.debug("Enrich loop finished: `%r`.", self)

    @abstractmethod
    def _merge(self) -> Generator[None, tuple[str, list[UpdatedAtId]], None]:
        """Method to merge data. Send data to transformer. Receive data from enricher."""
        pipe = self.transform_pipe()
        next(pipe)

        with self.pg_conn.cursor() as cur:
            try:
                while True:
                    last_updated, rows = yield
                    rows: list[UpdatedAtId]
                    cur.execute(
                        """
                            SELECT
                                fw.id,
                                fw.rating,
                                fw.title,
                                fw.description,
                                fw.type,
                                fw.creation_date,
                                fw.file_path,
                                fw.age_limit,
                                COALESCE (
                                   json_agg(
                                       DISTINCT jsonb_build_object(
                                           'id', g.id,
                                           'name', g.name
                                       )
                                   ) FILTER (WHERE g.id is not null),
                                   '[]'
                                ) as genres,
                                COALESCE (
                                   json_agg(
                                       DISTINCT jsonb_build_object(
                                           'id', p.id,
                                           'name', p.full_name
                                       )
                                   ) FILTER (WHERE p.id is not null AND pfw.role = 'director'),
                                   '[]'
                                ) as directors,
                                COALESCE (
                                   json_agg(
                                       DISTINCT jsonb_build_object(
                                           'id', p.id,
                                           'name', p.full_name
                                       )
                                   ) FILTER (WHERE p.id is not null AND pfw.role = 'actor'),
                                   '[]'
                                ) as actors,
                                COALESCE (
                                   json_agg(
                                       DISTINCT jsonb_build_object(
                                           'id', p.id,
                                           'name', p.full_name
                                       )
                                   ) FILTER (WHERE p.id is not null AND pfw.role = 'writer'),
                                   '[]'
                                ) as writers
                            FROM
                                content.film_work fw
                            LEFT JOIN
                                content.person_film_work pfw ON pfw.film_work_id = fw.id
                            LEFT JOIN
                                content.person p ON p.id = pfw.person_id
                            LEFT JOIN
                                content.genre_film_work gfw ON gfw.film_work_id = fw.id
                            LEFT JOIN
                                content.genre g ON g.id = gfw.genre_id
                            WHERE
                               fw.id IN %s
                            GROUP BY
                                fw.id;
                        """,
                        [tuple([row.id for row in rows])],  # psycopg2 is awesome ;<)
                    )
                    while results := cur.fetchmany(self.extract_chunk):
                        pipe.send((last_updated, [Filmwork(**result) for result in results]))
            except GeneratorExit:
                logger.debug("Merge loop finished: `%r`.", self)
