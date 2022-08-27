from http import HTTPStatus

import pytest
from api.messages import message
from core.config import settings
from db.db_models import Role


@pytest.fixture
def access_headers(client):
    login_url = settings.API_URL + 'auth/login'
    login_response = client.post(login_url, json={"email": "admin@admin.com", "password": "password"})
    access_token = login_response.json.get('tokens').get('access_token')
    access_headers = {'Authorization': f'Bearer {access_token}'}
    return access_headers


def test_get_roles(app, client, test_db, roles_data, access_headers):
    roles_url = settings.API_URL + 'roles/'
    response = client.get(roles_url, headers=access_headers)
    data = response.json
    assert response.status_code == HTTPStatus.OK
    assert len(data.get('roles')) == Role.query.count()
    assert data.get('roles')[0]['name'] == roles_data[1].name
    assert data.get('roles')[1]['name'] == roles_data[2].name


def test_get_role_by_name(app, client, test_db, roles_data, access_headers):
    role_url = settings.API_URL + f'roles/{roles_data[1].name}'
    response = client.get(role_url, headers=access_headers)
    data = response.json
    assert response.status_code == HTTPStatus.OK
    assert data.get('name') == roles_data[1].name
    assert data.get('description') == roles_data[1].description
    assert data.get('id') == str(roles_data[1].id)


def test_create_role(app, client, test_db, roles_data, access_headers):
    create_role_url = settings.API_URL + 'roles/'
    valid_data = {'name': 'New test role', 'description': 'New role description'}
    response = client.post(create_role_url, headers=access_headers, json=valid_data)
    data = response.json
    assert response.status_code == HTTPStatus.OK
    assert data.get('name') == valid_data.get('name')
    assert data.get('description') == valid_data.get('description')


def test_remove_role(app, client, test_db, roles_data, access_headers):
    delete_role_url = settings.API_URL + f'roles/{str(roles_data[2].id)}'
    response = client.delete(delete_role_url, headers=access_headers)
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_update_role(app, client, test_db, roles_data, access_headers):
    update_role_url = settings.API_URL + f'roles/{str(roles_data[2].id)}'
    valid_data = {'name': 'Update test role', 'description': 'Update role description'}
    response = client.patch(update_role_url, headers=access_headers, json=valid_data)
    data = response.json
    assert response.status_code == HTTPStatus.OK
    assert data.get('name') == valid_data.get('name')
    assert data.get('description') == valid_data.get('description')


def test_add_role_to_user(app, client, test_db, roles_data, test_user, access_headers):
    add_role_url = settings.API_URL + f'users/{str(test_user[0].id)}/roles/{str(roles_data[2].id)}'
    response = client.post(add_role_url, headers=access_headers)
    assert response.status_code == HTTPStatus.OK
    assert 'id' in response.json.keys()


def test_remove_role_from_user(app, client, test_db, roles_data, access_headers):
    add_role_url = settings.API_URL + f'users/{str(roles_data[4].id)}/roles/{str(roles_data[2].id)}'
    response = client.delete(add_role_url, headers=access_headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json.get('message') == message('success_delete_role', str(roles_data[2].id), str(roles_data[4].id))
