from functools import lru_cache
from typing import Optional

from aioredis import Redis
from services.abstract_cache import AsyncCacheStorage

redis: Optional[Redis] = None


class RedisCacher(AsyncCacheStorage):
    def __init__(self, redis_: Redis):
        self._redis = redis_

    async def get(self, key, *args, **kwargs):
        return await self._redis.get(key, *args, **kwargs)

    async def set(self, key, value, *, expire=0, pexpire=0, exist=None, **kwargs):
        await self._redis.set(key=key, value=value, expire=expire, pexpire=pexpire, exist=exist, **kwargs)


async def get_redis() -> Redis:
    return redis


@lru_cache
def get_redis_cacher() -> RedisCacher:
    return RedisCacher(redis)
