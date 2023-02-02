import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection

from postgres_saver import PostgresSaver
from extractor import SQLiteExtractor
from models import Filmwork, Genre, Person, GenreFilmwork, PersonFilmwork
from utils import sqlite_conn_context, psql_conn_context


def load_from_sqlite(
    connection: sqlite3.Connection, pg_conn: _connection, models: list[type[Any]], no_trigger_list: list[type[Any]]
):
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_extractor = SQLiteExtractor(connection)
    pg_saver = PostgresSaver(pg_conn)

    generator_list = []
    for model in models:
        generator_list.append(sqlite_extractor.extract(model))

    with pg_saver.silence_table_triggers(no_trigger_list):
        with ThreadPoolExecutor() as pool:
            pool.map(pg_saver.save, generator_list, timeout=10)


def setup_main() -> tuple[str, dict[str, str], list[type[Any]], list[type[Any]]]:
    load_dotenv(dotenv_path=".env")

    sqlite_db = os.getenv("SQLITE_DB_NAME", "sqlite_to_postgres/db.sqlite")
    pg_dsl = {
        "dbname": os.getenv("ADMIN_PANEL_POSTGRES_DB"),
        "user": os.getenv("ADMIN_PANEL_POSTGRES_USER"),
        "password": os.getenv("ADMIN_PANEL_POSTGRES_PASSWORD"),
        "host": os.getenv("ADMIN_PANEL_POSTGRES_HOST"),
        "port": os.getenv("ADMIN_PANEL_POSTGRES_PORT"),
    }

    models = [Filmwork, Genre, Person, GenreFilmwork, PersonFilmwork]
    no_trigger_list = [
        # Bypass FK constraint
        GenreFilmwork,
        PersonFilmwork,
    ]

    return sqlite_db, pg_dsl, models, no_trigger_list


if __name__ == "__main__":
    sqlite_db, pg_dsl, models, no_trigger_list = setup_main()
    with sqlite_conn_context(sqlite_db) as sqlite_conn, psql_conn_context(pg_dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn, models, no_trigger_list)
