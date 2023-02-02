import psycopg2
from dateutil.parser import parse
from psycopg2.extras import DictCursor

from load_data import setup_main, load_from_sqlite
from extractor import SQLiteExtractor, PostgresExtractor
from utils import sqlite_conn_context


def test_load_data():
    sqlite_db, pg_dsl, models, no_trigger_list = setup_main()

    with sqlite_conn_context(sqlite_db) as sqlite_conn, psycopg2.connect(
        **pg_dsl, cursor_factory=DictCursor
    ) as pg_conn:

        # exec main
        load_from_sqlite(sqlite_conn, pg_conn, models, no_trigger_list)

        sqlite_extractor = SQLiteExtractor(sqlite_conn)
        psql_extractor = PostgresExtractor(pg_conn)

        for model in models:
            expected = []
            generator = sqlite_extractor.extract(model)
            while data := next(generator, None):
                expected.extend(data)

            actual = []
            generator = psql_extractor.extract(model)
            while data := next(generator, None):
                actual.extend(data)

            for data in expected:
                # We get date as str from SQLlit, so we just parse it to datetime
                if hasattr(data, "created_at"):
                    data.created_at = parse(data.created_at)

                if hasattr(data, "updated_at"):
                    data.updated_at = parse(data.updated_at)

            assert len(expected) != 0, f"Expected size is zero for: {model.table_name}"
            assert len(actual) != 0, f"Actual size is zero for: {model.table_name}"
            assert len(actual) == len(expected), f"Invalid actual size for: {model.table_name}"
            assert actual == expected, f"Invalid actual content for: {model.table_name}"


if __name__ == "__main__":
    test_load_data()
