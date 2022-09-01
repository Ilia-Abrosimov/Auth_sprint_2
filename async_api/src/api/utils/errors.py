from http import HTTPStatus
from typing import Any, Dict, Optional

from fastapi import HTTPException
from pydantic import UUID4, BaseModel


class NotFoundException(HTTPException):
    def __init__(self, model: type(BaseModel), item_id: UUID4, headers: Optional[Dict[str, Any]] = None,) -> None:
        super().__init__(
            status_code=HTTPStatus.NOT_FOUND, detail=f'{model.__name__} with id = {item_id} not found', headers=headers
        )


class UnauthorizedError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED, detail='Bearer Token Error')


class AccessError(HTTPException):
    def __init__(self, role: str) -> None:
        super().__init__(status_code=HTTPStatus.FORBIDDEN, detail=f'For {role} only')


class AuthResponseError(HTTPException):
    def __init__(self, message: str = 'Auth response error') -> None:
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=message)
