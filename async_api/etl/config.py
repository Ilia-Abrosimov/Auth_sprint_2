import backoff
import psycopg2
from settings import settings

PG_DSN = {
    'dbname': settings.db.name,
    'user': settings.db.user,
    'password': settings.db.password,
    'host': settings.db.host,
    'port': settings.db.port,
}
ELASTIC_CONFIG = settings.elasticsearch
REDIS_CONFIG = settings.redis
BACKOFF_CONFIG = {'wait_gen': backoff.expo, 'exception': psycopg2.OperationalError}
BATCH_SIZE = settings.batch_size
INDEXES = settings.indexes
FREQUENCY = settings.frequency
REDIS_KEY = settings.redis_key
