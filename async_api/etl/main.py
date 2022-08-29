import datetime
import time

from config import BATCH_SIZE, ELASTIC_CONFIG, FREQUENCY, INDEXES, PG_DSN, REDIS_CONFIG, REDIS_KEY
from etl.etl import ETL
from etl.queries import get_genres_query, get_movies_query, get_persons_query
from etl.state import RedisStorage, State
from loguru import logger


def main():
    state = State(RedisStorage(REDIS_CONFIG, key=REDIS_KEY))
    while True:
        logger.info('Start')
        for index in INDEXES:
            if index == 'movies':
                query = get_movies_query(state.get_state(index, default=datetime.datetime.min))
            elif index == 'genres':
                query = get_genres_query(state.get_state(index, default=datetime.datetime.min))
            elif index == 'persons':
                query = get_persons_query(state.get_state(index, default=datetime.datetime.min))
            etl = ETL(pg_dsn=PG_DSN, elastic_config=ELASTIC_CONFIG, state=state, index=index)
            etl.process(query=query, batch_size=BATCH_SIZE)
        logger.info(f'Sleep ({FREQUENCY}s)...')
        time.sleep(FREQUENCY)


if __name__ == '__main__':

    main()
