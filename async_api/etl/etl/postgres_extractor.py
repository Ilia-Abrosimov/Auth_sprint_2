from typing import Iterator, Tuple

import backoff
import psycopg2
import psycopg2.extras
from config import BACKOFF_CONFIG
from es.models import GenresES, MoviesES, PersonsES
from psycopg2.extensions import connection as _connection

es_models = {'movies': MoviesES, 'genres': GenresES, 'persons': PersonsES}


class PostgresExtractor:
    def __init__(self, pg_conn: _connection, index: str):
        self._conn = pg_conn
        self._cursor = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        self._index = index

    @backoff.on_exception(**BACKOFF_CONFIG)
    def extract(self, query: str, batch_size: int) -> Iterator[Tuple[Tuple[dict, str]]]:
        self._cursor.itersize = batch_size
        self._cursor.execute(query)
        while rows := self._cursor.fetchmany(batch_size):
            yield ((es_models[self._index](**row).dict(by_alias=True), str(row['updated_at'])) for row in rows)
