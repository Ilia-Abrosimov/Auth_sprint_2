from api.v1.utils import oauth_login
from core.config import settings
from extensions import oauth
from flask import Blueprint, url_for

oauth.register(
    name='google',
    server_metadata_url=settings.GOOGLE_AUTH_URL,
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

oauth_google = Blueprint('oauth/google', __name__, url_prefix='/api/v1/oauth/google')


@oauth_google.route('/login')
def login():
    redirect_uri = url_for('oauth/google.auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


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
