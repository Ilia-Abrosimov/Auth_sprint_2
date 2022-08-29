import json
from http import HTTPStatus

import pytest
from tests.functional.testdata.data_for_es import films
from tests.functional.utils.models import FilmReviewResponseModel

from .errors import INVALID_PAGINATION_PositiveInt_ERROR, not_found_error


@pytest.mark.asyncio
async def test_films_list(make_get_request):
    response = await make_get_request('/films')
    sorted_films = sorted(films, key=lambda film: film['imdb_rating'], reverse=True)
    responsed_films = [FilmReviewResponseModel(**film) for film in response.body]
    assert response.status == HTTPStatus.OK
    assert len(response.body) == len(responsed_films)
    for i in range(len(responsed_films)):
        assert str(responsed_films[i].id) == sorted_films[i]['id']
        assert responsed_films[i].title == sorted_films[i]['title']
        assert responsed_films[i].imdb_rating == sorted_films[i]['imdb_rating']


@pytest.mark.asyncio
async def test_film_detail(make_get_request):
    film_id = films[0].get("id")
    response = await make_get_request(f"/films/{film_id}")
    assert response.status == HTTPStatus.OK
    for key in response.body:
        assert response.body[key] == films[0][key]


@pytest.mark.asyncio
async def test_unknown_film_id(make_get_request):
    wrong_film_id = '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07fa'
    response = await make_get_request(f"/films/{wrong_film_id}")
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body.get('detail') == not_found_error('film', wrong_film_id)


@pytest.mark.asyncio
async def test_films_page_size(make_get_request):
    params = {'page[size]': 1}
    response = await make_get_request('/films', params=params)
    assert response.status == HTTPStatus.OK
    assert len(response.body) == params['page[size]']
    for i in range(len(response.body)):
        for field in response.body[i]:
            assert response.body[i][field] == films[i][field]


@pytest.mark.asyncio
async def test_films_page_size_invalid(make_get_request):
    params = {'page[size]': -1}
    response = await make_get_request('/films', params=params)
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('detail')[0]['msg'] == INVALID_PAGINATION_PositiveInt_ERROR


@pytest.mark.asyncio
async def test_films_page_number(make_get_request):
    params = {'page[size]': 1, 'page[number]': 2}
    response = await make_get_request('/films', params=params)
    sorted_films = sorted(films, key=lambda film: film['imdb_rating'], reverse=True)
    assert response.status == HTTPStatus.OK
    assert len(response.body) == params['page[size]']
    for i in range(len(response.body)):
        for field in response.body[i]:
            assert response.body[i][field] == sorted_films[i + 1][field]


@pytest.mark.asyncio
async def test_films_page_number_invalid(make_get_request):
    params = {'page[size]': 1, 'page[number]': -2}
    response = await make_get_request('/films', params=params)
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('detail')[0]['msg'] == INVALID_PAGINATION_PositiveInt_ERROR


@pytest.mark.asyncio
async def test_films_sort(make_get_request):
    params = {'sort_string': 'imdb_rating'}
    response = await make_get_request('/films', params=params)
    assert response.status == HTTPStatus.OK
    assert len(response.body) == len(films)
    sorted_films = sorted(films, key=lambda film: film['imdb_rating'])
    for i in range(len(response.body)):
        for field in response.body[i]:
            assert response.body[i][field] == sorted_films[i][field]


@pytest.mark.asyncio
async def test_films_sort_invalid_field(make_get_request):
    params = {'sort_string': 'genre'}
    response = await make_get_request('/films', params=params)
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('detail')[0]['msg'] == (
        "value is not a valid enumeration member; permitted: '-imdb_rating', 'imdb_rating'")


@pytest.mark.asyncio
async def test_films_list_with_cache(make_get_request, redis_client):
    film_id = films[0].get("id")
    api_response = await make_get_request(f"/films/{film_id}")
    redis_response = await redis_client.get(f"movies:{film_id}")
    redis_data = json.loads(redis_response)
    assert api_response.status == HTTPStatus.OK
    assert len(api_response.body) == len(redis_data)
    for field in api_response.body:
        assert api_response.body[field] == redis_data[field]
