from http import HTTPStatus
from typing import Callable, Type
from functools import wraps

from flask import request
from flask_restplus import abort

from marshmallow import Schema as MarshmallowSchema
from marshmallow.exceptions import ValidationError


def marshmallow_parse(schema_class: Type[MarshmallowSchema], field: str,
                      *mm_args, **mm_kwargs) -> Callable:
    """
    Takes the request body json and converts in into an entity object
    :param field: the parameter name to use for the entity
    :param schema_class: Type[MarshmallowSchema]: The marshmallow schema for the conversion
    :return: a decorated function
    """
    schema = schema_class(*mm_args, **mm_kwargs)

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args, **kwargs):
            if not request.json:
                abort(HTTPStatus.BAD_REQUEST, 'Request body not json')

            try:
                kwargs[field], errors = schema.load(request.json)
                if errors:
                    abort(HTTPStatus.BAD_REQUEST, errors=errors)
            except ValidationError as e:
                abort(HTTPStatus.BAD_REQUEST, errors=e.normalized_messages())

            return function(*args, **kwargs)

        return wrapper

    return decorator
