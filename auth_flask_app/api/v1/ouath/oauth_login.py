from enum import Enum
from http import HTTPStatus

from api.v1.ouath.providers import Google, Yandex
from flask import Blueprint, abort, jsonify, make_response


class SocialNetworkProvider(Enum):
    Yandex = 'yandex'
    Google = 'google'


def get_providers(provider: str):
    if provider == SocialNetworkProvider.Google.name.lower():
        return Google()
    if provider == SocialNetworkProvider.Yandex.name.lower():
        return Yandex()
    abort(make_response(jsonify(message=f'provider {provider} not found'), HTTPStatus.BAD_REQUEST))


oauth_bp = Blueprint('oauth', __name__, url_prefix='/api/v1/oauth')


@oauth_bp.route('<string:provider_name>/login', methods=['GET'])
def login_by_social_network(provider_name: str):
    provider = get_providers(provider_name)
    return provider.login()
