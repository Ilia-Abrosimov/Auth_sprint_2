from datetime import datetime
from functools import wraps
from http import HTTPStatus

from db.db import redis_db
from flask import abort, jsonify, make_response, request

REQUEST_LIMIT_PER_MINUTE = 20


def rate_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pipe = redis_db.pipeline()
        now = datetime.now()
        key = f'{request.headers.get("Authorization")}:{now.minute}'
        pipe.incr(key, 1)
        pipe.expire(key, 59)
        result = pipe.execute()
        request_number = result[0]
        if request_number > REQUEST_LIMIT_PER_MINUTE:
            abort(make_response(jsonify(message="too many requests"), HTTPStatus.TOO_MANY_REQUESTS))
        ret = func(*args, **kwargs)
        return ret

    return wrapper
