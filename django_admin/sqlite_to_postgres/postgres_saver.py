import logging
from contextlib import contextmanager
from dataclasses import asdict
from typing import Any, Generator

from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2.errors import lookup
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_values
from psycopg2.sql import SQL, Identifier

logger = logging.getLogger(__file__)


class PostgresSaver:
    def __init__(self, connection: _connection):
        self.connection = connection

    def save(self, data_generator: Generator[list[Any], None, None]) -> None:
        """

        Args:
            data_generator: generator of filled table models

        Returns: None

        """
        cursor = self.connection.cursor()

        while data := next(data_generator, None):
            # Get table name and column list from dataclass
            table_name = data[0].table_name
            columns = ", ".join(list(asdict(data[0]).keys()))
            query = SQL(f"INSERT INTO content.{{table_name}} ({columns}) VALUES %s").format(
                table_name=Identifier(table_name)
            )

            # Get insert data from dataclass
            insert_data = [tuple(asdict(x).values()) for x in data]

            try:
                execute_values(cursor, query, insert_data)
                self.connection.commit()
            except lookup(UNIQUE_VIOLATION):
                logger.critical("UNIQUE_VIOLATION, %s, %s", query, insert_data)
                self.connection.rollback()

    def disable_trigger(self, table_name):
        query = SQL("ALTER TABLE content.{table} DISABLE TRIGGER ALL;").format(table=Identifier(table_name))
        self.connection.cursor().execute(query)

    def enable_trigger(self, table_name):
        query = SQL("ALTER TABLE content.{table} ENABLE TRIGGER ALL;").format(table=Identifier(table_name))
        self.connection.cursor().execute(query)

    @contextmanager
    def silence_table_triggers(self, models) -> None:
        """Method to bypass commit problems when filling DB, e.g. FK constraints"""
        for model in models:
            self.disable_trigger(model.table_name)

        yield

        for model in models:
            self.enable_trigger(model.table_name)
