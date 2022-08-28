import json
from functools import wraps
from typing import Any, Callable

from core.config import settings
from db.redis import get_redis
from pydantic import BaseModel


def serializer(item: Any) -> Any:
    if type(item) in (list, tuple):
        ret = []
        for one in item:
            ret.append(serializer(one))
    elif isinstance(item, BaseModel):
        ret = item.dict()
    else:
        ret = item
    return ret


async def _item_from_cache(key: str) -> Any:
    redis = await get_redis()
    data = await redis.get(key)
    if not data:
        return None
    return data


async def _put_item_to_cache(key: str, item: str, ttl: int):
    redis = await get_redis()
    await redis.set(key, item, expire=ttl)


def key_builder(keywords: str):
    def inner(func_name: str, *args, **kwargs) -> str:
        return f'func_{func_name}:' + ':'.join([f'{kwargs[x]}' for x in kwargs if x in keywords.split(',')])

    return inner


def cache(response_model: type(BaseModel),
          key_builder: Callable,
          ttl: int = settings.DEFAULT_CACHE_TTL):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            key = key_builder(func.__name__, **kwargs)
            if item := await _item_from_cache(key):
                return response_model.parse_raw(item)
            ret = await func(*args, **kwargs)
            await _put_item_to_cache(key=key, item=json.dumps(serializer(ret)), ttl=ttl)
            return ret

        return inner

    return wrapper
