from http import HTTPStatus
from typing import Any, Generic, Optional, Type, TypeVar, Union

from api.messages import message
from flask import abort, jsonify, make_response
from flask_marshmallow import Schema
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.exc import IntegrityError

ModelType = TypeVar('ModelType', bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=Schema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Schema)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Marshmallow model (schema) class
        """
        self.model = model

    def get(self, id_: Any) -> ModelType:
        result = self.model.query.filter_by(id=id_).first()
        if result:
            return result
        abort(make_response(jsonify(message=message('not_found_data', id_)), HTTPStatus.NOT_FOUND))

    def get_multi(
            self, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        return self.model.query.offset(skip).limit(limit).all()

    def create(self, db: SQLAlchemy, *, obj_in: CreateSchemaType) -> Optional[ModelType]:
        try:
            db.session.add(obj_in)
            db.session.commit()
            db.session.refresh(obj_in)
            return obj_in
        except IntegrityError:
            abort(make_response(jsonify(message=message('obj_exists', obj_in)), HTTPStatus.CONFLICT))

    def update(
            self,
            db: SQLAlchemy,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = UpdateSchemaType.dump(obj_in)
        for field in db_obj.__dict__:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        try:
            db.session.add(db_obj)
            db.session.commit()
            db.session.refresh(db_obj)
            return db_obj
        except IntegrityError:
            abort(make_response(jsonify(message=message('obj_not_update', obj_in)), HTTPStatus.CONFLICT))

    def remove(self, db: SQLAlchemy, *, id_: Any) -> None:
        obj = self.get(id_)
        db.session.delete(obj)
        db.session.commit()
