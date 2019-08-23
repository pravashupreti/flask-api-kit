from http import HTTPStatus
from flask_restplus import Api
from marshmallow.exceptions import ValidationError

from api.utilities.common import log_error
from api.exceptions.generic_exception import GenericException

authorizations = {
    "apiKey": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "template": "Bearer {apiKey}",
    }
}

api = Api(
    version="1",
    title="Flask Api Kit",
    description="Flask api kit",
    prefix="/api",
    authorizations=authorizations)


@api.errorhandler(ValidationError)
def payload_validation_exception(error: ValidationError):
    status = HTTPStatus.NOT_ACCEPTABLE
    log_error(error, status)
    return {"messages": error.messages}, HTTPStatus.NOT_ACCEPTABLE


@api.errorhandler(GenericException)
def generic_exception(error: GenericException):
    log_error(error)
    return error.get_response()
