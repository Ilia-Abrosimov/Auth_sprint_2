from datetime import timedelta
from http import HTTPStatus

import crud
from api.messages import message
from core.config import settings
from core.rate_limit import rate_limit
from db.db import db, redis_db
from db.db_models import LoginHistory, Profile, User
from extensions import jwt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from marshmallow import ValidationError
from schemas.auth import (login_history_schema, password_schema, profile_schema, user_profile_schema, user_role_schema,
                          user_schema)

from .utils import generate_tokens

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth.route('/signup', methods=['POST'])
@rate_limit
def signup():
    data = request.json
    try:
        user_profile = user_profile_schema.load(data)
        user = user_schema.load(user_profile, session=db.session)
        profile = profile_schema.load(user_profile, session=db.session)
    except ValidationError as error:
        response = jsonify(message=error.messages)
        response.status_code = HTTPStatus.BAD_REQUEST
        return response
    user_exists = User.query.filter_by(email=user_profile.get('email')).first() is not None
    if user_exists:
        response = jsonify(message=message('email_exists', user_profile.get('email')))
        response.status_code = HTTPStatus.BAD_REQUEST
        return response
    user.set_password(data.get('password'))
    profile.user = user
    db.session.add_all([user, profile])
    db.session.commit()
    response = jsonify(result=[user_schema.dump(user), profile_schema.dump(profile)],
                       message=message('success_register'))
    response.status_code = HTTPStatus.CREATED
    return response


@auth.route('/login', methods=['POST'])
@rate_limit
def login():
    data = request.json
    try:
        user_profile = user_profile_schema.load(data)
    except ValidationError as error:
        response = jsonify(message=error.messages)
        response.status_code = HTTPStatus.BAD_REQUEST
        return response
    user = User.query.filter_by(email=user_profile.get('email')).first()
    if user is None or not user.check_password(user_profile.get('password')):
        response = jsonify(message=message('bad_auth_data', user_profile.get('email')))
        response.status_code = HTTPStatus.UNAUTHORIZED
        return response
    access_token, refresh_token = generate_tokens(user)
    response = jsonify(message=message('JWT_generated'),
                       tokens={'access_token': access_token, "refresh_token": refresh_token})
    response.status_code = HTTPStatus.OK
    login_history = LoginHistory(user_id=user.id, user_agent=str(request.user_agent))
    db.session.add(login_history)
    db.session.commit()
    return response


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = redis_db.get(jti)
    return token_in_redis is not None


@auth.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
@rate_limit
def update_token():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    access_token, refresh_token = generate_tokens(user)
    response = jsonify(message=message('JWT_generated'),
                       tokens={'access_token': access_token, 'refresh_token': refresh_token})
    response.status_code = HTTPStatus.OK
    jti = get_jwt()["jti"]
    at = get_jwt()["at"]
    redis_db.set(jti, "", ex=timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRES))
    redis_db.set(at, "", ex=timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRES))
    return response


@auth.route("/logout", methods=['DELETE'])
@jwt_required(refresh=True)
@rate_limit
def logout():
    jti = get_jwt()["jti"]
    at = get_jwt()["at"]
    redis_db.set(jti, "", ex=timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRES))
    redis_db.set(at, "", ex=timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRES))
    return jsonify(message=message('revoked_token'))


@auth.route("/password-change/<uuid:user_id>", methods=['PATCH'])
@jwt_required()
@rate_limit
def change_password(user_id):
    data = request.json
    try:
        passwords = password_schema.load(data)
    except ValidationError as error:
        response = jsonify(message=error.messages)
        response.status_code = HTTPStatus.BAD_REQUEST
        return response
    user = User.query.filter_by(id=user_id).first()
    id_by_token = get_jwt_identity()
    user_by_token = User.query.filter_by(id=id_by_token).first()
    if user is not user_by_token:
        response = jsonify(message=message('foreign_token'))
        response.status_code = HTTPStatus.BAD_REQUEST
        return response
    if user is None or not user.check_password(passwords.get('old_password')):
        response = jsonify(message=message('user_not_exists'))
        response.status_code = HTTPStatus.BAD_REQUEST
        return response
    user.set_password(passwords.get('new_password'))
    db.session.add(user)
    db.session.commit()
    response = jsonify(message=message('success_change_password'))
    response.status_code = HTTPStatus.CREATED
    return response


@auth.route("/profile-change/<uuid:profile_id>", methods=['PATCH'])
@jwt_required()
@rate_limit
def change_profile(profile_id):
    try:
        profile_schema.load(request.json)
    except ValidationError as error:
        response = jsonify(message=error.messages)
        response.status_code = HTTPStatus.BAD_REQUEST
        return response
    profile = Profile.query.filter_by(id=profile_id).first()
    id_by_token = get_jwt_identity()
    if profile is None:
        response = jsonify(message=message('not_found_profile'))
        response.status_code = HTTPStatus.BAD_REQUEST
        return response
    if str(profile.user_id) != id_by_token:
        response = jsonify(message=message('foreign_profile'))
        response.status_code = HTTPStatus.BAD_REQUEST
        return response
    for key in request.json:
        setattr(profile, key, request.json[key])
    db.session.add(profile)
    db.session.commit()
    response = jsonify(message=message('success_change_profile'))
    response.status_code = HTTPStatus.CREATED
    return response


@auth.route("/login-history/<uuid:user_id>", methods=['GET'])
@jwt_required()
@rate_limit
def get_login_history(user_id):
    page = request.args.get('page', 1, type=int)
    histories = LoginHistory.query.filter_by(user_id=user_id).paginate(page=page, per_page=2)
    id_by_token = get_jwt_identity()
    if str(histories.items[0].user_id) != id_by_token:
        response = jsonify(message=message('foreign_history'))
        response.status_code = HTTPStatus.BAD_REQUEST
        return response
    response = jsonify(result=[login_history_schema.dump(history) for history in histories.items],
                       prev=histories.prev_num, next=histories.next_num, total_items=histories.total,
                       total_pages=histories.pages)
    response.status_code = HTTPStatus.OK
    return response


@auth.route("/verify-jwt", methods=['GET'])
@jwt_required()
@rate_limit
def verify_jwt():
    """Получение параметров доступа пользователя.
    ---
    tags:
      - auth
    definitions:
      VerifyJWT:
        type: object
        properties:
          id:
            type: string
            example: 9c2da540-3535-4597-b6f6-bb3e1a385e65
          is_superuser:
            type: boolean
            example: false
          role:
            type: string
            example: user
    responses:
      200:
        description: "Successful operation"
        schema:
          $ref: '#/definitions/VerifyJWT'
    """
    result = user_role_schema.dump(crud.user.get(get_jwt_identity()))
    role_id = crud.user.get_role_id(get_jwt_identity(), mute=True)
    if role_id:
        result['role'] = crud.role.get(role_id).name
    else:
        result['role'] = 'user'
    return result


@auth.route("/hello", methods=["GET"])
@jwt_required()
@rate_limit
def hello():
    return 'Hello'
