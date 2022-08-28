import asyncio

import pytest
from elasticsearch import AsyncElasticsearch
from tests.functional.settings import settings
from tests.functional.testdata.data_for_es import data_for_elastic
from tests.functional.testdata.indexes import indexes


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=f'{settings.ES_HOST}:{settings.ES_PORT}')

    yield client
    await client.close()


@pytest.fixture(autouse=True)
async def create_es_data(es_client):
    for item in ['movies', 'genres', 'persons']:
        index = indexes.get(item)
        if not await es_client.indices.exists(index=item):
            await es_client.indices.create(index=item, body=index)
    await es_client.bulk(data_for_elastic())
    await asyncio.sleep(1)
    yield
    await es_client.indices.delete(index="_all")
