from flask import url_for, Blueprint, jsonify, request
from extensions import oauth
from api.v1.utils import generate_tokens, generate_random_string
from db.db_models import SocialAccount, User, LoginHistory, Profile
from api.messages import message
from http import HTTPStatus
from db.db import db
from core.config import settings

print(settings.YANDEX_CLIENT_ID)
oauth.register(
    name='yandex',
    client_id=settings.YANDEX_CLIENT_ID,  # спрятать
    client_secret=settings.YANDEX_CLIENT_SECRET,  # спрятать
    access_token_url='https://oauth.yandex.ru/token',
    authorize_url='https://oauth.yandex.ru/authorize'
)

oauth_yandex = Blueprint('oauth', __name__, url_prefix='/api/v1/oauth/yandex')


@oauth_yandex.route('/login')
def login():
    redirect_uri = url_for('oauth.auth', _external=True)
    return oauth.yandex.authorize_redirect(redirect_uri)


@oauth_yandex.route('/auth')
def auth():
    token = oauth.yandex.authorize_access_token()
    resp = oauth.yandex.get(f'https://login.yandex.ru/info?format=json&jwt_secret={token}',
                            token=token)
    resp.raise_for_status()
    yandex_profile = resp.json()
    social_id = yandex_profile.get('id')
    email = yandex_profile.get('default_email')
    social_account = SocialAccount.query.filter_by(social_id=social_id).first()
    if social_account:
        user = User.query.filter_by(id=social_account.user.id).first()
        access_token, refresh_token = generate_tokens(user)
        response = jsonify(message=message('JWT_generated'),
                           tokens={'access_token': access_token, "refresh_token": refresh_token})
        response.status_code = HTTPStatus.OK
        login_history = LoginHistory(user_id=user.id, user_agent=str(request.user_agent))
        db.session.add(login_history)
        db.session.commit()
        return response
    user = User(email=email)
    user.set_password(generate_random_string())
    profile = Profile(first_name=yandex_profile.get('first_name'), last_name=yandex_profile.get('last_name'))
    profile.user = user
    social_account = SocialAccount(social_id=yandex_profile.get('id'), social_name='Yandex')
    social_account.user = user
    login_history = LoginHistory(user_agent=str(request.user_agent))
    login_history.user = user
    db.session.add_all([user, profile, social_account, login_history])
    db.session.commit()
    access_token, refresh_token = generate_tokens(user)
    response = jsonify(message=message('JWT_generated'),
                       tokens={'access_token': access_token, "refresh_token": refresh_token})
    response.status_code = HTTPStatus.OK
    return response
