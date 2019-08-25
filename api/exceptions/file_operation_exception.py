from api.exceptions.generic_exception import GenericException


class FileOperationException(GenericException):
    # TODO what does this even mean?
    message = "File operation exception"
