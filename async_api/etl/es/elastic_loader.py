from typing import Iterator, Tuple

import backoff
from config import BACKOFF_CONFIG
from elasticsearch import Elasticsearch, helpers
from etl.state import State
from loguru import logger


class ElasticLoader:
    def __init__(self, elastic_connection: Elasticsearch, state: State, index: str):
        self._elastic_connection = elastic_connection
        self._state = state
        self._index = index

    @backoff.on_exception(**BACKOFF_CONFIG)
    def upload_data(self, data: Iterator[Tuple[Tuple[dict, str]]], batch_size: int) -> None:
        for batch in data:
            docs = self._generate_docs(batch, self._index)

            lines, errors = helpers.bulk(
                client=self._elastic_connection,
                actions=docs,
                index=self._index,
                chunk_size=batch_size,
                stats_only=False,
            )
            if lines == 0:
                logger.info('Nothing to update')
            else:
                logger.info(f'{lines} lines saved')
            if errors:
                logger.error('Errors while write to elasticsearch:')
                for error in errors:
                    logger.error(f'{error}')

    def _generate_docs(self, data: Tuple[Tuple[dict, str]], key: str):
        last_updated = None
        for movie, updated_at in data:
            last_updated = updated_at
            yield movie
        if last_updated:
            self._state.set_state(key, last_updated)
