from api.v1.utils import oauth_login
from core.config import settings
from extensions import oauth
from flask import Blueprint, url_for

oauth_yandex = Blueprint('oauth/yandex', __name__, url_prefix='/api/v1/oauth/yandex')


class Yandex:
    oauth.register(
        name='yandex',
        client_id=settings.YANDEX_CLIENT_ID,
        client_secret=settings.YANDEX_CLIENT_SECRET,
        access_token_url=settings.YANDEX_AUTH_URL,
        authorize_url='https://oauth.yandex.ru/authorize'
    )

    def login(self):
        redirect_uri = url_for('oauth/yandex.auth', _external=True)
        print(redirect_uri)
        return oauth.yandex.authorize_redirect(redirect_uri)

    @staticmethod
    @oauth_yandex.route('/auth')
    def auth():
        token = oauth.yandex.authorize_access_token()
        resp = oauth.yandex.get(f'https://login.yandex.ru/info?format=json&jwt_secret={token}',
                                token=token)
        resp.raise_for_status()
        yandex_profile = resp.json()
        social_profile = {
            'social_id': yandex_profile['id'],
            'email': yandex_profile['default_email'],
            'first_name': yandex_profile['first_name'],
            'last_name': yandex_profile['last_name']
        }
        response = oauth_login(social_profile, 'yandex')
        return response


oauth_google = Blueprint('oauth/google', __name__, url_prefix='/api/v1/oauth/google')


class Google:
    oauth.register(
        name='google',
        server_metadata_url=settings.GOOGLE_AUTH_URL,
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    def login(self):
        redirect_uri = url_for('oauth/google.auth', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)

    @staticmethod
    @oauth_google.route('/auth')
    def auth():
        token = oauth.google.authorize_access_token()
        social_profile = {
            'social_id': token['userinfo']['sub'],
            'email': token['userinfo']['email'],
            'first_name': token['userinfo']['given_name'],
            'last_name': token['userinfo']['family_name']
        }
        response = oauth_login(social_profile, 'google')
        return response
