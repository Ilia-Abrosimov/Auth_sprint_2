import aioredis
import pytest
from tests.functional.settings import settings


@pytest.fixture(scope='session')
async def redis_client():
    redis = await aioredis.create_redis_pool((settings.REDIS_HOST, settings.REDIS_PORT), minsize=10, maxsize=20)
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest.fixture(autouse=True)
async def redis_reset(redis_client):
    await redis_client.flushall()
