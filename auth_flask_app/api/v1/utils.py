import string
from secrets import choice as secrets_choice

import jwt as decode_jwt
from core.config import settings
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
