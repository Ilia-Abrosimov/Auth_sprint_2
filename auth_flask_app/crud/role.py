from http import HTTPStatus

from api.messages import message
from crud.base import BaseCRUD
from db.db_models import Role
from flask import abort, jsonify, make_response
from schemas.role import RoleSchema


class RoleCRUD(BaseCRUD[Role, RoleSchema, RoleSchema]):
    def get_by_name(self, name: str):
        result = self.model.query.filter_by(name=name).first()
        if result:
            return result
        abort(make_response(jsonify(message=message('role_not_found', name)), HTTPStatus.NOT_FOUND))


role = RoleCRUD(Role)
