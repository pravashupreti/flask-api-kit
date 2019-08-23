from http import HTTPStatus

from api.exceptions.generic_exception import GenericException


class InvalidPayloadException(GenericException):
    status = HTTPStatus.NOT_ACCEPTABLE
