import re
import traceback
from functools import partial
from http import HTTPStatus
from typing import Optional, Type

from flask import jsonify, make_response, request
from logzero import logger
from werkzeug.exceptions import HTTPException

from api.exceptions.generic_exception import GenericException
from api.models.base_model import BaseModel
from api.schemas.base_schema import BaseSchema
from config import Config
from api.exceptions.api_errors import APIException


def json_response(data=None, status: HTTPStatus = HTTPStatus.OK, headers=None):
    """
    Generate json response with given payload, status and headers

    :param data: Data to response
    :type data: Any
    :param status: Response http status
    :type status: HTTPStatus
    :param headers: response header
    """
    headers = headers or {}
    if "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"
    return make_response(jsonify(data), status, headers)


def _get_error_status(error: Exception) -> HTTPStatus:
    if isinstance(error, HTTPException):
        return HTTPStatus(error.code)
    if isinstance(error, GenericException):
        return error.status
    if isinstance(error, APIException):
        return HTTPStatus(error.status_code)

    return HTTPStatus.INTERNAL_SERVER_ERROR


def _get_error_data(error: Exception) -> Optional[dict]:
    if isinstance(error, APIException):
        return error.to_dict()
    # TODO add other types of errors to this
    return None


def log_error(error: Exception, status: HTTPStatus = None) -> None:
    if not status:
        status = _get_error_status(error)

    tb = traceback.format_exc(limit=5)
    path = request.path
    query_string = str(request.query_string, "utf-8")
    path = "?".join([path, query_string]) if query_string else path

    args = ("%s %s %s %s %s \n %s", request.remote_addr, request.method,
            path, status.value, str(error), tb)

    meta_data = {
        "request": {
            "address": request.remote_addr,
            "method": request.method,
            "path": path,
            "status": status.value,
        }
    }

    error_data = _get_error_data(error)

    if error_data:
        meta_data["error"] = error_data

    if status.value < 500:        
        logger.warning(*args)
        return

    logger.error(*args)


def id_validator(model: Type[BaseModel]) -> callable:
    return partial(BaseSchema.object_id_exists, model=model)


def unique_field_validator(model: Type[BaseModel], field: str) -> callable:
    return partial(BaseSchema.unique_field_exists, model=model, field=field)


def sorted_alpha_numerical_list(l):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)
    