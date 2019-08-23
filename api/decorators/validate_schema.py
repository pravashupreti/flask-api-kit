from functools import wraps

from flask import request

from jsonschema import validate, exceptions
from api.exceptions import InvalidPayloadException


# TODO this should be removed Marshmallow validators should be used instead.
def validate_schema(schema):
    """
    A decorator to validate request body with given schema.
    :param schema
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            payload = request.json if request.data else {}

            try:
                validate(payload, schema)
            except exceptions.ValidationError as error:
                raise InvalidPayloadException(detail={
                    "validator": error.validator,
                    "message": error.message})

            return func(*args, **kwargs)

        return wrapper

    return decorator
