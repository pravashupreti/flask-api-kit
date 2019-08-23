"""

Handles common Flask and data errors by returning appropriate HTTP error codes
with a JSON body. Usage:

    from api.exceptions.api_errors import UnprocessableEntity
    raise UnprocessableEntity('Could not parse JSON')

"""
from typing import Tuple
from abc import abstractmethod

from http import HTTPStatus as httplib
from flask import jsonify, Response


class APIException(Exception):
    status_code = 500

    @abstractmethod
    def to_dict(self) -> dict:
        return {}


def handle_unauthorized(_):
    response = jsonify(message='Unauthorized.')
    response.status_code = httplib.UNAUTHORIZED
    return response


def handle_page_not_found(_):
    response = jsonify(message='Not found.')
    response.status_code = httplib.NOT_FOUND
    return response


def handle_method_not_allowed(_):
    response = jsonify(message='Method not allowed.')
    response.status_code = httplib.METHOD_NOT_ALLOWED
    return response


class UnprocessableEntity(APIException):
    status_code = httplib.UNPROCESSABLE_ENTITY

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        return rv


class IntegrityError(UnprocessableEntity):
    def __init__(self, field, message=None):
        Exception.__init__(self)
        self.field = field
        self.message = message
        self.status_code = httplib.UNPROCESSABLE_ENTITY

    def to_dict(self):
        rv = dict()

        if self.message:
            rv['message'] = self.message

        rv['errors'] = [dict(
            key=self.field,
            validator='unique_constraint',
        )]
        return rv


class BadUpload(APIException):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class BadInvite(APIException):
    status_code = 422

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class BadRequest(APIException):
    status_code = httplib.BAD_REQUEST

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class FormError(Exception):
    """Raise when an error processing a form occurs."""

    def __init__(self, errors):
        self.errors = errors


def handle_form_error(e):
    return jsonify(dict(errors=e.errors)), 400


def handle_api_error(error: APIException) -> Response:
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
