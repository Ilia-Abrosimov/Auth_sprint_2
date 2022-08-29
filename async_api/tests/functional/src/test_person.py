import json
from http import HTTPStatus

import pytest
from tests.functional.src.errors import INVALID_PAGINATION_PositiveInt_ERROR, not_found_error
from tests.functional.testdata.data_for_es import persons
from tests.functional.utils.models import FilmReviewResponseModel, PersonResponseModel


@pytest.mark.asyncio
async def test_person_detail(make_get_request):
    person_id = persons[0].get('id')
    response = await make_get_request(f'/persons/{person_id}')
    assert response.status == HTTPStatus.OK
    PersonResponseModel(**response.body)
    for key in ('id', 'name', 'role', 'film_ids'):
        assert response.body[key] == persons[0][key]


@pytest.mark.asyncio
async def test_unknown_person_id(make_get_request):
    person_id = '01234567-0123-4567-89ab-cdef01234567'
    response = await make_get_request(f'/persons/{person_id}')
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body.get('detail') == not_found_error('person', person_id)


@pytest.mark.asyncio
async def test_person_films(make_get_request):
    person_id = '26e83050-29ef-4163-a99d-b546cac208f8'
    response = await make_get_request(f'/persons/{person_id}/film')
    assert response.status == HTTPStatus.OK
    responsed_person_films = [FilmReviewResponseModel(**item) for item in response.body]
    assert len(responsed_person_films) == 2
    assert {str(x.id) for x in responsed_person_films} == {
        '3d825f60-9fff-4dfe-b294-1a45fa1e115d',
        '025c58cd-1b7e-43be-9ffb-8571a613579b',
    }
    assert response.body == [
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
    ]


@pytest.mark.asyncio
async def test_person_films_page_size(make_get_request):
    person_id = '26e83050-29ef-4163-a99d-b546cac208f8'
    params = {'page[size]': 1}
    response = await make_get_request(f'/persons/{person_id}/film', params=params)
    assert response.status == HTTPStatus.OK
    assert len(response.body) == 1
    assert response.body == [
        {
            'id': '3d825f60-9fff-4dfe-b294-1a45fa1e115d',
            'title': 'Star Wars: Episode IV - A New Hope',
            'imdb_rating': 8.6,
        }
    ]


@pytest.mark.asyncio
async def test_person_films_page_size_invalid(make_get_request):
    person_id = '26e83050-29ef-4163-a99d-b546cac208f8'
    params = {'page[size]': -1}
    response = await make_get_request(f'/persons/{person_id}/film', params=params)
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('detail')[0]['msg'] == INVALID_PAGINATION_PositiveInt_ERROR


@pytest.mark.asyncio
async def test_person_films_page_number(make_get_request):
    person_id = '26e83050-29ef-4163-a99d-b546cac208f8'
    params = {'page[size]': 1, 'page[number]': 2}
    response = await make_get_request(f'/persons/{person_id}/film', params=params)
    assert response.status == HTTPStatus.OK
    assert len(response.body) == 1
    assert response.body == [
        {
            'id': '025c58cd-1b7e-43be-9ffb-8571a613579b',
            'title': 'Star Wars: Episode VI - Return of the Jedi',
            'imdb_rating': 8.3,
        }
    ]


@pytest.mark.asyncio
async def test_person_films_page_number_invalid(make_get_request):
    person_id = '26e83050-29ef-4163-a99d-b546cac208f8'
    params = {'page[size]': 1, 'page[number]': -1}
    response = await make_get_request(f'/persons/{person_id}/film', params=params)
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('detail')[0]['msg'] == INVALID_PAGINATION_PositiveInt_ERROR


@pytest.mark.asyncio
async def test_person_detail_with_cache(make_get_request, redis_client):
    person_id = '26e83050-29ef-4163-a99d-b546cac208f8'
    api_response = await make_get_request(f'/persons/{person_id}')
    redis_response = await redis_client.get(f'persons:{person_id}')
    redis_data = json.loads(redis_response)
    assert api_response.status == HTTPStatus.OK
    assert len(api_response.body) == len(redis_data)
    for key in ('id', 'name', 'role', 'film_ids'):
        assert api_response.body[key] == redis_data[key]
