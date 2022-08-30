from api.v1.utils import oauth_login
from core.config import settings
from extensions import oauth
from flask import Blueprint, url_for

oauth.register(
    name='yandex',
    client_id=settings.YANDEX_CLIENT_ID,
    client_secret=settings.YANDEX_CLIENT_SECRET,
    access_token_url='https://oauth.yandex.ru/token',
    authorize_url='https://oauth.yandex.ru/authorize'
)

oauth_yandex = Blueprint('oauth/yandex', __name__, url_prefix='/api/v1/oauth/yandex')


@oauth_yandex.route('/login')
def login():
    redirect_uri = url_for('oauth/yandex.auth', _external=True)
    return oauth.yandex.authorize_redirect(redirect_uri)


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
