import backoff
from redis import Redis
from redis.exceptions import ConnectionError
from tests.functional.settings import settings
from tests.functional.utils.tools import backoff_hdlr


@backoff.on_exception(wait_gen=backoff.expo, exception=ConnectionError, on_backoff=backoff_hdlr)
def wait_redis():
    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    if not redis.ping():
        raise ConnectionError('Redis is not ready yet...')
    redis.close()


if __name__ == '__main__':
    wait_redis()
