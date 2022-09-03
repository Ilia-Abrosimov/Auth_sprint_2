from http import HTTPStatus

import crud
from api.messages import message
from core.rate_limit import rate_limit
from db.db import db
from flask import Blueprint, Response, abort, jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from schemas.role import full_role_schema, role_schema, roles_schema

role_bp = Blueprint('roles', __name__, url_prefix='/api/v1/roles')


@role_bp.route('/', methods=['GET'])
@jwt_required()
@rate_limit
def get_roles():
    """Получение списка всех ролей.
    ---
    tags:
      - roles
    definitions:
      Roles:
        type: object
        properties:
          roles:
            type:
              array
            items:
              $ref: '#/definitions/Role'
      Role:
        type: object
        properties:
          name:
            type: string
            example: admin
          description:
            type: string
            example: administrator
    responses:
      200:
        description: "Successful operation"
        schema:
          $ref: '#/definitions/Roles'
    """
    if not crud.user.is_superuser(get_jwt_identity()):
        if not crud.user.is_admin(get_jwt_identity()):
            abort(make_response(jsonify(message=message('access_error')), HTTPStatus.FORBIDDEN))

    result = roles_schema.dump(crud.role.get_multi())
    return {'roles': result}


@role_bp.route('/<role_name>', methods=['GET'])
@jwt_required()
@rate_limit
def get_role_by_name(role_name):
    """Получение роли по названию.
    ---
    tags:
      - roles
    parameters:
      - name: role_name
        in: path
        required: true
        type: string
    definitions:
      RoleFull:
        type: object
        properties:
          id:
            type: uuid
            example: 05ff941d-21ff-408e-afb5-a3240df05438
          name:
            type: string
            example: admin
          description:
            type: string
            example: administrator
    responses:
      200:
        description: "Successful operation"
        schema:
          $ref: '#/definitions/RoleFull'
    """
    if not crud.user.is_superuser(get_jwt_identity()):
        if not crud.user.is_admin(get_jwt_identity()):
            abort(make_response(jsonify(message=message('access_error')), HTTPStatus.FORBIDDEN))

    result = full_role_schema.dump(crud.role.get_by_name(role_name))
    return result


@role_bp.route('/', methods=['POST'])
@jwt_required()
@rate_limit
def create_role():
    """Создание роли.
    ---
    tags:
      - roles
    parameters:
      - name: new_role
        in: body
        required: true
        type: string
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      200:
        description: "Successful operation"
        schema:
          $ref: '#/definitions/Role'
    """
    if not crud.user.is_superuser(get_jwt_identity()):
        if not crud.user.is_admin(get_jwt_identity()):
            abort(make_response(jsonify(message=message('access_error')), HTTPStatus.FORBIDDEN))

    data = request.json
    try:
        role = role_schema.load(data)
    except ValidationError as error:
        print(error.messages)
        response = jsonify(message=error.messages)
        response.status_code = HTTPStatus.BAD_REQUEST
        return response

    return jsonify(role_schema.dump(crud.role.create(db, obj_in=role)))


@role_bp.route('/<uuid:role_id>', methods=['DELETE'])
@jwt_required()
@rate_limit
def remove_role(role_id):
    """Удаление роли.
    ---
    tags:
      - roles
    parameters:
      - name: role_id
        in: path
        required: true
        type: string
    responses:
      204:
        description: "Successful operation"
    """
    if not crud.user.is_superuser(get_jwt_identity()):
        if not crud.user.is_admin(get_jwt_identity()):
            abort(make_response(jsonify(message=message('access_error')), HTTPStatus.FORBIDDEN))

    crud.role.remove(db, id_=role_id)
    return Response(status=HTTPStatus.NO_CONTENT)


@role_bp.route('/<uuid:role_id>', methods=['PATCH'])
@jwt_required()
@rate_limit
def update_role(role_id):
    """Изменение роли.
    ---
    tags:
      - roles
    parameters:
      - name: role_id
        in: path
        type: uuid
      - name: update_role
        in: body
        required: true
        type: string
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      200:
        description: "Successful operation"
        schema:
          $ref: '#/definitions/Role'
    """
    if not crud.user.is_superuser(get_jwt_identity()):
        if not crud.user.is_admin(get_jwt_identity()):
            abort(make_response(jsonify(message=message('access_error')), HTTPStatus.FORBIDDEN))

    role = crud.role.get(role_id)
    data = request.json
    result = role_schema.dump(crud.role.update(db, db_obj=role, obj_in=data))
    return jsonify(result)
