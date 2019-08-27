from http import HTTPStatus

from api.exceptions.generic_exception import GenericException


class AuthException(GenericException):
    status = HTTPStatus.UNAUTHORIZED


class AuthInvalidHeader(AuthException):
    message = "The header could not be verified"


class AuthTokenExpired(AuthException):
    message = "The Bearer Token has expired"


class AuthInvalidClaim(AuthException):
    message = "Incorrect claims, please check the audience and issuer"


class AuthHeaderMissing(AuthException):
    message = "Authorization header missing."


class AuthMissingScope(AuthException):
    def __init__(self, scope: str, **kwargs):
        super().__init__("requires scope '{}'".format(scope), **kwargs)


class AuthPermissionDenied(GenericException):
    status = HTTPStatus.FORBIDDEN
    message = "You don't have permission for this"
