import datetime
import time
from contextlib import closing

from psycopg2.extras import DictCursor

from etl.extractors.base_extractor import BaseExtractor
from etl.loaders.base_loader import BaseLoader
from etl.transformers.base_transformer import BaseTransformer
from helpers.state import State, RedisStorage
from settings import Settings
from storage_clients.elasticsearch_client import ElasticsearchClient
from storage_clients.postgres_client import PostgresClient
from storage_clients.redis_client import RedisClient


def etl(
    settings: Settings,
    elk_index: str,
    extractor_type: type[BaseExtractor],
    transformer_type: type[BaseTransformer],
    loader_type: type[BaseLoader],
    state_key: str,
    timeout: int = 2.5,
):
    """Factory of etl pipes"""

    with closing(PostgresClient(settings.postgres_dsn, cursor_factory=DictCursor)) as pg_conn, closing(
        ElasticsearchClient(settings.elasticsearch_dsn)
    ) as elk_conn, closing(RedisClient(settings.redis_dsn)) as redis_conn:
        pg_conn: PostgresClient
        elk_conn: ElasticsearchClient
        redis_conn: RedisClient

        state = State(RedisStorage(redis_conn), state_key)

        if not state.exists():
            state.set(str(datetime.datetime.min))

        loader = loader_type(
            elk_conn=elk_conn,
            state=state,
            elk_index=elk_index,
            load_chunk=settings.load_chunk,
        )
        transformer = transformer_type(
            load_pipe=loader.load,
        )
        extractor = extractor_type(
            pg_conn=pg_conn,
            state=state,
            extract_chunk=settings.extract_chunk,
            transform_pipe=transformer.transform,
        )
        while True:
            extractor.extract()
            time.sleep(timeout)
