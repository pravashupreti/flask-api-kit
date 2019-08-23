from http import HTTPStatus

from flask import Flask, Response, jsonify
from werkzeug.exceptions import HTTPException

from api.exceptions.generic_exception import GenericException
from api.utilities.common import log_error

from api.exceptions.api_errors import APIException, handle_api_error


def _handle_error(error: Exception) -> Response:
    """
    Handles any errors that were not caught by restplus
    :param error:
    :return:
    """
    log_error(error)
    if isinstance(error, GenericException):
        return error.get_response()

    if isinstance(error, HTTPException):
        response = jsonify({
            'status': error.code,
            'error': error.name,
            'message': error.description
        })

        response.status_code = error.code
        return response

    if isinstance(error, APIException):
        return handle_api_error(error)

    status = HTTPStatus.INTERNAL_SERVER_ERROR

    response = jsonify({
        'status': status.value,
        'error': status.phrase,
        'message': status.description,
    })
    response.status_code = status.value

    return response


def init_error_handlers(app: Flask) -> Flask:

    app.register_error_handler(Exception, _handle_error)

    return app
