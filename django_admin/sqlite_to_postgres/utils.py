import sqlite3
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor


@contextmanager
def sqlite_conn_context(db_path: str):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row

    yield conn

    conn.close()


@contextmanager
def psql_conn_context(pg_dsl: dict[str, str]):
    conn = psycopg2.connect(**pg_dsl, cursor_factory=DictCursor)

    yield conn

    conn.close()
