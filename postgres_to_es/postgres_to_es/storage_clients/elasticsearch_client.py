import elastic_transport
from elasticsearch import Elasticsearch, helpers
from pydantic import AnyHttpUrl

from helpers.backoff import backoff, reconnect as storage_reconnect
from helpers.exceptions import ElasticsearchNotConnectedError
from helpers.logger import LoggerFactory
from storage_clients.base_client import AbstractStorage

logger = LoggerFactory().get_logger()


class ElasticsearchClient(AbstractStorage):
    """Layer over Elasticsearch for backoff implementation and closing connections."""

    base_exceptions = elastic_transport.ConnectionError
    _connection: Elasticsearch

    def __init__(self, dsn: AnyHttpUrl, *args, **kwargs):
        super().__init__(dsn, *args, **kwargs)

    @property
    def is_connected(self) -> bool:
        return self._connection and self._connection.ping()

    @backoff(exceptions=(base_exceptions, ElasticsearchNotConnectedError))
    def connect(self) -> None:
        self._connection = Elasticsearch(self.dsn, *self.args, **self.kwargs)

        if not self.is_connected:
            # client is lazy, need to check it
            raise ElasticsearchNotConnectedError(f"Connection is not properly established for: `{self.__repr__()}`")

        logger.info("Established new connection for: `%r.", self)

    def reconnect(self) -> None:
        super().reconnect()

    @backoff(exceptions=base_exceptions)
    def close(self) -> None:
        super().close()

    @backoff(exceptions=(base_exceptions, elastic_transport.SerializationError))
    @storage_reconnect
    def index_exists(self, index: str) -> None:
        return self._connection.indices.exists(index=index)

    @backoff(exceptions=(base_exceptions, elastic_transport.SerializationError))
    @storage_reconnect
    def index_create(self, index: str, body: dict) -> None:
        return self._connection.indices.create(index=index, body=body)

    @backoff(exceptions=(base_exceptions, elastic_transport.SerializationError))
    @storage_reconnect
    def bulk(self, actions: list, *args, **kwargs) -> None:
        helpers.bulk(self._connection, *args, actions=actions, **kwargs)
