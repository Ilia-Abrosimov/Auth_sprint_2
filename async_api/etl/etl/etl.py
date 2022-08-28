from typing import Iterator, Optional, Tuple

import backoff
import psycopg2
from elasticsearch import Elasticsearch, NotFoundError
from es.elastic_loader import ElasticLoader
from etl.postgres_extractor import PostgresExtractor
from etl.state import State
from loguru import logger
from psycopg2.extensions import connection as pg_connection
from settings import ElasticConfig


class ETL:
    def __init__(self, pg_dsn: dict, elastic_config: ElasticConfig, state: State, index: str):
        self.pg_dsn = pg_dsn
        self._elastic_config: ElasticConfig = elastic_config
        self._state: State = state
        self._pg_conn: Optional[pg_connection] = None
        self._index = index

    def elasticsearch_ready(self) -> bool:
        try:
            elastic_connection = Elasticsearch([f'{self._elastic_config.host}:{self._elastic_config.port}'])
            elastic_connection.indices.get(self._index)

        except NotFoundError as error:
            logger.error(error)
            return False

        return True

    def process(self, query: str, batch_size: int):
        if not self.elasticsearch_ready():
            return
        data_from_postgres = self.extract(query=query, batch_size=batch_size)
        self.load(data_from_postgres, batch_size=batch_size)
        self.close_pg_conn()
        logger.info('Postgres closed.')

    @logger.catch
    @backoff.on_exception(backoff.expo, exception=psycopg2.OperationalError)
    def load(self, data, batch_size: int):
        elastic_connection = Elasticsearch([f'{self._elastic_config.host}:{self._elastic_config.port}'])
        elastic_loader = ElasticLoader(elastic_connection=elastic_connection, state=self._state, index=self._index)
        elastic_loader.upload_data(data, batch_size=batch_size)

    @logger.catch
    @backoff.on_exception(backoff.expo, exception=psycopg2.OperationalError)
    def extract(self, query: str, batch_size: int) -> Iterator[Tuple[Tuple[dict, str]]]:
        # подключение к БД
        logger.info('Begin connecting to postgres.')
        extractor = PostgresExtractor(pg_conn=self.get_pg_conn(), index=self._index)
        logger.info('Postgres connected.')
        data_generator = extractor.extract(query=query, batch_size=batch_size)

        return data_generator

    def close_pg_conn(self):
        if self._pg_conn is not None:
            self._pg_conn.close()

    def get_pg_conn(self):
        if self._pg_conn is None or self._pg_conn.closed:
            self._pg_conn = psycopg2.connect(**self.pg_dsn)
        return self._pg_conn
