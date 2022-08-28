import asyncio
from dataclasses import dataclass
from typing import Optional

import aiohttp
import pytest
from multidict import CIMultiDictProxy

from .settings import settings

SERVICE_URL = f'http://{settings.API_HOST}:{settings.API_PORT}'
pytest_plugins = ("tests.functional.plugins.redis", "tests.functional.plugins.elastic")


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + '/api/v1' + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
