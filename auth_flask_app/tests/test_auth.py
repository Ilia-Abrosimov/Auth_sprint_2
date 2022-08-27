from http import HTTPStatus

from api.messages import message
from core.config import settings
from db.db_models import Profile


def test_signup(app, client, test_db):
    valid_data = {
        "email": "Test@test.com",
        "first_name": "Test first_name",
        "last_name": "Test last_name",
        "phone": "+7123456789",
        "password": "qwerty"
    }
    url = settings.API_URL + 'auth/signup'
    response = client.post(url, json=valid_data)
    data = response.json
    assert response.status_code == HTTPStatus.CREATED
    assert data.get('result')[0]['email'] == valid_data.get('email')
    assert data.get('result')[1]['first_name'] == valid_data.get('first_name')
    invalid_data = {
        "first_name": "Test first_name",
        "last_name": "Test last_name",
        "phone": 56789,
        "password": "qwerty"
    }
    invalid_message = {'message': {'email': ['Missing data for required field.'], 'phone': ['Not a valid string.']}}
    response = client.post(url, json=invalid_data)
    data = response.json
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data.get('message')['email'] == invalid_message.get('message')['email']
    assert data.get('message')['phone'] == invalid_message.get('message')['phone']
    duplicate_data_response = client.post(url, json=valid_data)
    assert duplicate_data_response.status_code == HTTPStatus.BAD_REQUEST
    data = duplicate_data_response.json
    assert data.get('message') == message('email_exists', valid_data.get('email'))


def test_login(app, client, test_db, test_user):
    valid_data = {
        "email": "Test@test.com",
        "password": "qwerty"
    }
    url = settings.API_URL + 'auth/login'
    response = client.post(url, json=valid_data)
    data = response.json
    assert response.status_code == HTTPStatus.OK
    assert data.get('message') == message('JWT_generated')
    assert 'access_token' in data.get('tokens').keys()
    assert 'refresh_token' in data.get('tokens').keys()
    invalid_data = {
        "login": "Test@test.com",
        "password": "qwerty"
    }
    invalid_message = {'message': {'email': ['Missing data for required field.'], 'login': ['Unknown field.']}}
    response = client.post(url, json=invalid_data)
    data = response.json
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data.get('message') == invalid_message.get('message')
    unknown_user_data = {
        "email": "Unknown@test.com",
        "password": "qwerty"
    }
    response = client.post(url, json=unknown_user_data)
    data = response.json
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert data.get('message') == message('bad_auth_data', unknown_user_data.get('email'))


def test_update_token(app, client, test_db, test_user):
    url = settings.API_URL + 'auth/login'
    response = client.post(url, json={"email": "Test@test.com", "password": "qwerty"})
    refresh_token = response.json.get('tokens').get('refresh_token')
    headers = {'Authorization': f'Bearer {refresh_token}'}
    refresh_token_url = settings.API_URL + 'auth/refresh-token'
    news_token = client.post(refresh_token_url, headers=headers)
    data = news_token.json
    assert news_token.status_code == HTTPStatus.OK
    assert data.get('message') == message('JWT_generated')
    assert 'access_token' in data.get('tokens').keys()
    assert 'refresh_token' in data.get('tokens').keys()
    retry_request = client.post(refresh_token_url, headers=headers)
    assert retry_request.status_code == HTTPStatus.UNAUTHORIZED
    assert retry_request.json.get('msg') == 'Token has been revoked'


def test_logout(app, client, test_db, test_user):
    url = settings.API_URL + 'auth/login'
    response = client.post(url, json={"email": "Test@test.com", "password": "qwerty"})
    access_token = response.json.get('tokens').get('access_token')
    refresh_token = response.json.get('tokens').get('refresh_token')
    access_headers = {'Authorization': f'Bearer {access_token}'}
    refresh_headers = {'Authorization': f'Bearer {refresh_token}'}
    protect_url = settings.API_URL + 'auth/hello'
    authorized_response = client.get(protect_url, headers=access_headers)
    assert authorized_response.status_code == HTTPStatus.OK
    logout_url = settings.API_URL + 'auth/logout'
    logout_response = client.delete(logout_url, headers=refresh_headers)
    assert logout_response.status_code == HTTPStatus.OK
    assert logout_response.json.get('message') == message('revoked_token')
    authorized_response = client.get(protect_url, headers=access_headers)
    assert authorized_response.status_code == HTTPStatus.UNAUTHORIZED
    assert authorized_response.json.get('msg') == 'Token has been revoked'


def test_change_password(app, client, test_db, test_user):
    user_id = test_user[0].id
    login_url = settings.API_URL + 'auth/login'
    login_response = client.post(login_url, json={"email": "Test@test.com", "password": "qwerty"})
    access_token = login_response.json.get('tokens').get('access_token')
    access_headers = {'Authorization': f'Bearer {access_token}'}
    valid_data = {
        "old_password": "qwerty",
        "new_password": "qwerty123"
    }
    url = settings.API_URL + f'auth/password-change/{user_id}'
    response = client.patch(url, headers=access_headers, json=valid_data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json.get('message') == message('success_change_password')
    invalid_data = {
        "password": "qwerty",
        "new_password": "qwerty123"
    }
    invalid_message = {
        'message': {'old_password': ['Missing data for required field.'], 'password': ['Unknown field.']}}
    invalid_response = client.patch(url, headers=access_headers, json=invalid_data)
    assert invalid_response.status_code == HTTPStatus.BAD_REQUEST
    assert invalid_response.json.get('message') == invalid_message.get('message')
    invalid_user_id = test_user[1].id
    url = settings.API_URL + f'auth/password-change/{invalid_user_id}'
    response = client.patch(url, headers=access_headers, json=valid_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json.get('message') == message('foreign_token')


def test_change_profile(app, client, test_db, test_user):
    user_id = test_user[0].id
    login_url = settings.API_URL + 'auth/login'
    login_response = client.post(login_url, json={"email": "Test@test.com", "password": "qwerty"})
    access_token = login_response.json.get('tokens').get('access_token')
    access_headers = {'Authorization': f'Bearer {access_token}'}
    profile = Profile.query.filter_by(user_id=user_id).first()
    url = settings.API_URL + f'auth/profile-change/{profile.id}'
    valid_data = {
        "first_name": "Ivan",
        "last_name": "Ivanov"
    }
    assert profile.first_name != valid_data.get('first_name')
    assert profile.last_name != valid_data.get('last_name')
    response = client.patch(url, headers=access_headers, json=valid_data)
    assert response.json.get('message') == message('success_change_profile')
    assert response.status_code == HTTPStatus.CREATED
    updated_profile = Profile.query.filter_by(user_id=user_id).first()
    assert updated_profile.first_name == valid_data.get('first_name')
    assert updated_profile.last_name == valid_data.get('last_name')
    wrong_profile_id = '4434fe38-628a-46ff-be70-3d4d2f176e4e'
    invalid_url = settings.API_URL + f'auth/profile-change/{wrong_profile_id}'
    invalid_response = client.patch(invalid_url, headers=access_headers, json=valid_data)
    assert invalid_response.status_code == HTTPStatus.BAD_REQUEST
    assert invalid_response.json.get('message') == message('not_found_profile')
    another_profile_id = test_user[3].id
    invalid_url = settings.API_URL + f'auth/profile-change/{another_profile_id}'
    invalid_response = client.patch(invalid_url, headers=access_headers, json=valid_data)
    assert invalid_response.status_code == HTTPStatus.BAD_REQUEST
    assert invalid_response.json.get('message') == message('foreign_profile')


def test_login_history(app, client, test_db, test_user):
    user_id = test_user[0].id
    login_url = settings.API_URL + 'auth/login'
    for _ in range(5):
        client.post(login_url, json={"email": "Test@test.com", "password": "qwerty"})
    login_response = client.post(login_url, json={"email": "Test@test.com", "password": "qwerty"})
    access_token = login_response.json.get('tokens').get('access_token')
    access_headers = {'Authorization': f'Bearer {access_token}'}
    history_url = settings.API_URL + f'auth/login-history/{user_id}'
    history_response = client.get(history_url, headers=access_headers)
    data = history_response.json
    assert history_response.status_code == HTTPStatus.OK
    assert 'next' in data.keys()
    assert 'prev' in data.keys()
    assert 'result' in data.keys()
    assert 'total_items' in data.keys()
    assert 'total_pages' in data.keys()
    assert data.get('total_items') == 6
    assert data.get('total_pages') == 3
    login_url = settings.API_URL + 'auth/login'
    login_response = client.post(login_url, json={"email": "Test2@test.com", "password": "qwerty321"})
    access_token = login_response.json.get('tokens').get('access_token')
    access_headers = {'Authorization': f'Bearer {access_token}'}
    history_url = settings.API_URL + f'auth/login-history/{user_id}'
    history_response = client.get(history_url, headers=access_headers)
    assert history_response.status_code == HTTPStatus.BAD_REQUEST
    assert history_response.json.get('message') == message('foreign_history')
