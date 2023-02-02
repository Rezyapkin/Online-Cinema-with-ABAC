import logging
import sqlite3
from typing import Any, Iterator

from psycopg2.extensions import connection as _connection

logger = logging.getLogger(__file__)


class AbstractExtractor:
    CHUNK_SIZE = 50

    def __init__(self, connection):
        self.connection = connection

    @staticmethod
    def _fetch(data: list[Any], model: type[Any]) -> list[Any]:
        try:
            return [model(**dict(x)) for x in data]
        except Exception as e:
            logger.critical("Error during fetching data into mnodel:\n%s", e)
            raise e

    def extract(self, model: type[Any]) -> Iterator[list[Any]]:
        """
        Method to get data from DB by CHUNK_SIZe
        Args:
            model: class of table model, contains columns and table_name attr

        Returns: Iterator over chunked result

        """
        cursor = self.connection.cursor()

        try:
            cursor.execute(f"SELECT * FROM {model.table_name}")
        except sqlite3.Error as e:
            logger.critical("Error during executing query SQLite:\n%s", e)
            raise e

        try:
            while results := cursor.fetchmany(self.CHUNK_SIZE):
                yield self._fetch(results, model)
        except sqlite3.Error as e:
            logger.critical("Error during getting data from SQLite:\n%s", e)
            raise e

    def count(self, model: type[Any]) -> int:
        """
        Method to extract count of rows from table by its model
        Args:
            model: class of table model, contains columns and table_name attr

        Returns: Number of rows in table

        """
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {model.table_name}")
        return cursor.fetchone()[0]


class SQLiteExtractor(AbstractExtractor):
    def __init__(self, connection: sqlite3.Connection):
        super().__init__(connection)


class PostgresExtractor(AbstractExtractor):
    def __init__(self, connection: _connection):
        super().__init__(connection)
