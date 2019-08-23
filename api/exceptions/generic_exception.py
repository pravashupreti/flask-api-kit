from http import HTTPStatus
from typing import Union

from flask import jsonify, Response


class GenericException(Exception):

    status = HTTPStatus.INTERNAL_SERVER_ERROR
    message = None
    detail = None

    def __init__(
            self,
            message: str = None,
            detail: Union[str, dict] = None,
            status: HTTPStatus = None):

        super(GenericException, self).__init__(self)

        if message:
            self.message = message
        if detail:
            self.detail = detail
        if status:
            self.status = status

        if not self.detail:
            self.detail = self.status.phrase
        if not self.message:
            self.message = self.status.description

    def get_response(self) -> Response:
        response = jsonify(self.__dict__())
        response.status_code = self.status.value
        return response

    def __dict__(self) -> dict:
        return {
            'status': self.status.value,
            'detail': self.detail,
            'message': self.message,
        }

    def __str__(self) -> str:
        return str({
            'error': self.detail,
            'message': self.message
        })
