from http import HTTPStatus

from api.messages import message
from core.types import RoleTypes
from crud import role
from crud.base import BaseCRUD
from db.db_models import User, UsersRoles
from flask import abort, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from schemas.auth import UserSchema
from sqlalchemy.exc import IntegrityError


class UserCRUD(BaseCRUD[User, UserSchema, UserSchema]):
    def add_role(self, db: SQLAlchemy, user_id: str, role_id: str):
        self.get(user_id)
        role.get(role_id)
        db_obj = UsersRoles(user_id=user_id, role_id=role_id)
        try:
            db.session.add(db_obj)
            db.session.commit()
            db.session.refresh(db_obj)
            return db_obj
        except IntegrityError:
            abort(make_response(jsonify(message=message('obj_exists', db_obj)), HTTPStatus.CONFLICT))

    def remove_role(self, db: SQLAlchemy, user_id: str, role_id: str):
        role.get(role_id)
        db_obj = self.get(user_id)
        db_obj.role.delete()
        db.session.add(db_obj)
        db.session.commit()

    def has_role(self, user_id: str, role_id: str, mute=False) -> bool:
        db_obj = self.get(user_id)
        user_role = db_obj.role.first()
        if not user_role:
            if mute:
                return False
            abort(make_response(jsonify(message=message('obj_not_role', db_obj)), HTTPStatus.CONFLICT))
        user_role_id = user_role.role_id
        role.get(role_id)
        return user_role_id == role_id

    def is_admin(self, user_id: str) -> bool:
        admin = role.get_by_name(RoleTypes.ADMIN)
        return self.has_role(user_id=user_id, role_id=admin.id, mute=True)

    def is_superuser(self, user_id: str) -> bool:
        db_obj = self.get(user_id)
        if db_obj.is_superuser:
            return True
        return False


user = UserCRUD(User)
