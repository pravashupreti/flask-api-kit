from http import HTTPStatus

from api.exceptions.generic_exception import GenericException


class RowNotFoundException(GenericException):
    status = HTTPStatus.NOT_FOUND
    message = "The resource you requested could not be found"
