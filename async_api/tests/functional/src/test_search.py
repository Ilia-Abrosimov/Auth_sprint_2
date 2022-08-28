import json
from http import HTTPStatus

import pytest
from tests.functional.src.errors import INVALID_PAGINATION_PositiveInt_ERROR
from tests.functional.utils.models import FilmReviewResponseModel, PersonResponseModel


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'item_type,model,query,response_body',
    [
        (
            'films',
            FilmReviewResponseModel,
            'star',
            [
                {
                    'id': '3d825f60-9fff-4dfe-b294-1a45fa1e115d',
                    'title': 'Star Wars: Episode IV - A New Hope',
                    'imdb_rating': 8.6,
                },
                {
                    'id': '025c58cd-1b7e-43be-9ffb-8571a613579b',
                    'title': 'Star Wars: Episode VI - Return of the Jedi',
                    'imdb_rating': 8.3,
                },
            ],
        ),
        (
            'persons',
            PersonResponseModel,
            'Cushing',
            [
                {
                    'id': 'e039eedf-4daf-452a-bf92-a0085c68e156',
                    'name': 'Peter Cushing',
                    'role': ['actor'],
                    'film_ids': ['3d825f60-9fff-4dfe-b294-1a45fa1e115d'],
                }
            ],
        ),
        ('films', FilmReviewResponseModel, 'what', [],),
        ('persons', PersonResponseModel, 'sasha', []),
    ],
)
async def test_search_many(make_get_request, item_type, model, query, response_body):
    params = {'query': query}
    response = await make_get_request(f'/{item_type}/search', params=params)
    assert response.status == HTTPStatus.OK
    responsed_items = [model(**item) for item in response.body]
    assert len(responsed_items) == len(response_body)
    assert response.body == response_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'item_type,query,response_body',
    [
        (
            'films',
            'star',
            [
                {
                    'id': '3d825f60-9fff-4dfe-b294-1a45fa1e115d',
                    'title': 'Star Wars: Episode IV - A New Hope',
                    'imdb_rating': 8.6,
                }
            ],
        ),
        (
            'persons',
            'Cushing',
            [
                {
                    'id': 'e039eedf-4daf-452a-bf92-a0085c68e156',
                    'name': 'Peter Cushing',
                    'role': ['actor'],
                    'film_ids': ['3d825f60-9fff-4dfe-b294-1a45fa1e115d'],
                }
            ],
        ),
    ],
)
async def test_search_page_size(make_get_request, item_type, query, response_body):
    params = {'query': query, 'page[size]': 1}
    response = await make_get_request(f'/{item_type}/search', params=params)
    assert response.status == HTTPStatus.OK
    assert len(response.body) == len(response_body)
    assert response.body == response_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'item_type,query', [('films', ''), ('persons', '')],
)
async def test_search_page_size_invalid(make_get_request, item_type, query):
    params = {'query': query, 'page[size]': -1}
    response = await make_get_request(f'/{item_type}/search', params=params)
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('detail')[0]['msg'] == INVALID_PAGINATION_PositiveInt_ERROR


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'item_type,query,response_body',
    [
        (
            'films',
            'star',
            [
                {
                    'id': '025c58cd-1b7e-43be-9ffb-8571a613579b',
                    'title': 'Star Wars: Episode VI - Return of the Jedi',
                    'imdb_rating': 8.3,
                },
            ],
        ),
        ('persons', 'Cushing', [],),
    ],
)
async def test_search_page_number(make_get_request, item_type, query, response_body):
    params = {'query': query, 'page[size]': 1, 'page[number]': 2}
    response = await make_get_request(f'/{item_type}/search', params=params)
    assert response.status == HTTPStatus.OK
    assert len(response.body) == len(response_body)
    assert response.body == response_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'item_type,query', [('films', ''), ('persons', '')],
)
async def test_person_films_page_number_invalid(make_get_request, item_type, query):
    params = {'query': query, 'page[size]': 1, 'page[number]': -1}
    response = await make_get_request(f'/{item_type}/search', params=params)
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('detail')[0]['msg'] == INVALID_PAGINATION_PositiveInt_ERROR


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'item_type,query,redis_key',
    [
        ('films', 'star', 'func_search_films:imdb_rating:desc:2:1:star',),
        ('persons', 'Cushing', 'func_search_persons:2:1:Cushing',),
    ],
)
async def test_search_with_cache(make_get_request, item_type, query, redis_key, redis_client):
    params = {'query': query, 'page[size]': 2, 'page[number]': 1}
    api_response = await make_get_request(f'/{item_type}/search', params=params)
    redis_response = await redis_client.get(redis_key)
    redis_data = json.loads(redis_response)
    assert api_response.status == HTTPStatus.OK
    assert len(api_response.body) == len(redis_data)
    for i in range(len(api_response.body)):
        for key in api_response.body[i]:
            assert api_response.body[i][key] == redis_data[i][key]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query,response_body',
    [
        (
            'star',
            [
                {
                    'id': '025c58cd-1b7e-43be-9ffb-8571a613579b',
                    'title': 'Star Wars: Episode VI - Return of the Jedi',
                    'imdb_rating': 8.3,
                },
                {
                    'id': '3d825f60-9fff-4dfe-b294-1a45fa1e115d',
                    'title': 'Star Wars: Episode IV - A New Hope',
                    'imdb_rating': 8.6,
                },
            ],
        )
    ],
)
async def test_search_films_sort(make_get_request, query, response_body):
    params = {'query': query, 'sort_string': 'imdb_rating'}
    response = await make_get_request('/films/search', params=params)
    assert response.status == HTTPStatus.OK
    assert len(response.body) == len(response_body)
    assert response.body == response_body
