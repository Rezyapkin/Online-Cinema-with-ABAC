from psycopg2.sql import SQL, Identifier

from etl.extractors.base_extractor import BaseExtractor
from helpers.logger import LoggerFactory
from models.person import Person
from models.updated_at_id import UpdatedAtId

logger = LoggerFactory().get_logger()


class PersonExtractor(BaseExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.produce_table = "person"

    def extract(self) -> None:
        """Method to monitor data update in PGSQL Send data to enricher."""
        started = False

        with self.pg_conn.cursor() as cur:
            cur.execute(
                SQL(
                    """
                    SELECT
                        id,
                        full_name as name,
                        updated_at
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
                    pipe = self.transform_pipe()
                    next(pipe)
                    started = True

                last_updated = UpdatedAtId(**results[-1]).updated_at
                pipe.send((last_updated, [Person(**result) for result in results]))

            logger.info("Extract loop finished: `%r`. Going to start a new loop.", self)
