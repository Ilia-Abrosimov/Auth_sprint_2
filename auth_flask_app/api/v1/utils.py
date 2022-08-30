import string
from http import HTTPStatus
from secrets import choice as secrets_choice

import jwt as decode_jwt
from api.messages import message
from core.config import settings
from db.db import db
from db.db_models import LoginHistory, Profile, SocialAccount, User
from flask import Response, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token


def generate_tokens(user):
    access_token = create_access_token(identity=user.id)
    decode_access_token = decode_jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms="HS256")
    claims = {'at': decode_access_token['jti']}
    refresh_token = create_refresh_token(identity=user.id, additional_claims=claims)
    return access_token, refresh_token


def generate_random_string():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets_choice(alphabet) for _ in range(16))


def oauth_login(social_profile: dict[str, str], provider_name: str) -> Response:
    social_account = SocialAccount.query.filter_by(social_id=social_profile['social_id']).first()
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
    user = User(email=social_profile['email'])
    user.set_password(generate_random_string())
    profile = Profile(first_name=social_profile['first_name'], last_name=social_profile['last_name'])
    profile.user = user
    social_account = SocialAccount(social_id=social_profile['social_id'], social_name=provider_name)
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
