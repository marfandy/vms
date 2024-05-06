from rest_framework import permissions, status
from rest_framework.exceptions import APIException


class GenericException(APIException):
    """
    Generic exception with custom message
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = "error"


class InvalidLogin(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_code = "error"


class PuclicException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "error"


class ConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "error"
