import json
from http import HTTPStatus

import pytest
from tests.functional.src.errors import INVALID_PAGINATION_PositiveInt_ERROR, not_found_error
from tests.functional.testdata.data_for_es import genres


@pytest.mark.asyncio
async def test_genres_list(make_get_request):
    response = await make_get_request('/genres')
    assert response.status == HTTPStatus.OK
    assert len(response.body) == len(genres)
    for i in range(len(response.body)):
        assert response.body[i]['id'] == genres[i]['id']
        assert response.body[i]['name'] == genres[i]['name']


@pytest.mark.asyncio
async def test_genre_detail(make_get_request):
    genre_id = genres[0].get("id")
    response = await make_get_request(f"/genres/{genre_id}")
    assert response.status == HTTPStatus.OK
    for key in response.body:
        assert response.body[key] == genres[0][key]


@pytest.mark.asyncio
async def test_unknown_genre_id(make_get_request):
    wrong_genre_id = '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07fa'
    response = await make_get_request(f"/genres/{wrong_genre_id}")
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body.get('detail') == not_found_error('genre', wrong_genre_id)


@pytest.mark.asyncio
async def test_genres_page_size(make_get_request):
    params = {'page[size]': 1}
    response = await make_get_request('/genres', params=params)
    assert response.status == HTTPStatus.OK
    assert len(response.body) == params['page[size]']
    for i in range(len(response.body)):
        for field in response.body[i]:
            assert response.body[i][field] == genres[i][field]


@pytest.mark.asyncio
async def test_genres_page_size_invalid(make_get_request):
    params = {'page[size]': -1}
    response = await make_get_request('/genres', params=params)
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('detail')[0]['msg'] == INVALID_PAGINATION_PositiveInt_ERROR


@pytest.mark.asyncio
async def test_genres_page_number(make_get_request):
    params = {'page[size]': 1, 'page[number]': 2}
    response = await make_get_request('/genres', params=params)
    assert response.status == HTTPStatus.OK
    for i in range(len(response.body)):
        for field in response.body[i]:
            assert response.body[i][field] == genres[i+1][field]
    params_2 = {'page[size]': 1, 'page[number]': 3}
    response = await make_get_request('/genres', params=params_2)
    assert response.status == HTTPStatus.OK
    for i in range(len(response.body)):
        for field in response.body[i]:
            assert response.body[i][field] == genres[i+2][field]


@pytest.mark.asyncio
async def test_genres_page_number_invalid(make_get_request):
    params = {'page[size]': 1, 'page[number]': -2}
    response = await make_get_request('/genres', params=params)
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('detail')[0]['msg'] == INVALID_PAGINATION_PositiveInt_ERROR


@pytest.mark.asyncio
async def test_genres_list_with_cache(make_get_request, redis_client):
    film_id = genres[0].get("id")
    api_response = await make_get_request(f"/genres/{film_id}")
    redis_response = await redis_client.get(f"genres:{film_id}")
    redis_data = json.loads(redis_response)
    assert api_response.status == HTTPStatus.OK
    assert len(api_response.body) == len(redis_data)
    for field in api_response.body:
        assert api_response.body[field] == redis_data[field]
