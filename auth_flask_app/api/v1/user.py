from http import HTTPStatus

import crud
from api.messages import message
from db.db import db
from flask import Blueprint, abort, jsonify, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required
from schemas.auth import user_schema

user_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')


@user_bp.route('/<uuid:user_id>/roles/<uuid:role_id>', methods=['POST'])
@jwt_required()
def add_role_to_user(user_id, role_id):
    """Назначить пользователю роль.
    ---
    tags:
      - users
    parameters:
      - name: user_id
        in: path
        type: uuid
      - name: role_id
        in: path
        type: uuid
    definitions:
      UsersRole:
        type: object
        properties:
          id:
            type: uuid
            example: 05ff941d-21ff-408e-afb5-a3240df05438
    responses:
      200:
        description: "Successful operation"
        schema:
          $ref: '#/definitions/UsersRole'
    """
    if not crud.user.is_superuser(get_jwt_identity()):
        if not crud.user.is_admin(get_jwt_identity()):
            abort(make_response(jsonify(message=message('access_error')), HTTPStatus.FORBIDDEN))

    result = user_schema.dump(crud.user.add_role(db, user_id, role_id))
    return result


@user_bp.route('/<uuid:user_id>/roles/<uuid:role_id>', methods=['DELETE'])
@jwt_required()
def remove_role_from_user(user_id, role_id):
    """Отобрать у пользователя роль.
    ---
    tags:
      - users
    parameters:
      - name: user_id
        in: path
        type: uuid
      - name: role_id
        in: path
        type: uuid
    responses:
      200:
        description: "Successful operation"
    """
    if not crud.user.is_superuser(get_jwt_identity()):
        if not crud.user.is_admin(get_jwt_identity()):
            abort(make_response(jsonify(message=message('access_error')), HTTPStatus.FORBIDDEN))

    crud.user.remove_role(db, user_id, role_id)
    return make_response(jsonify(message=message('success_delete_role', role_id, user_id)), HTTPStatus.OK)


@user_bp.route('/<uuid:user_id>/roles/<uuid:role_id>', methods=['GET'])
@jwt_required()
def user_has_role(user_id, role_id):
    """Проверить наличие прав у пользователя.
    ---
    tags:
      - users
    parameters:
      - name: user_id
        in: path
        type: uuid
      - name: role_id
        in: path
        type: uuid
    definitions:
      HasRole:
        type: object
        properties:
          exists:
            type: boolean
            example: False
    responses:
      200:
        description: "Successful operation"
        schema:
          $ref: '#/definitions/HasRole'
    """
    if not crud.user.is_superuser(get_jwt_identity()):
        if not crud.user.is_admin(get_jwt_identity()):
            abort(make_response(jsonify(message=message('access_error')), HTTPStatus.FORBIDDEN))

    result = crud.user.has_role(user_id, role_id)
    return {'exists': result}
