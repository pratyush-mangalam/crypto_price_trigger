from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidTokenException(Exception):
    pass


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = "permission_denied"
    default_detail = "You do not have permission to perform this action."

    def __init__(self, detail=None, code=None):
        if isinstance(detail, str):
            detail = {"detail": detail}
        super().__init__(detail, code)
