from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException


class CustomPermissionDenied(APIException):
    status_code = 403
    default_detail = "Permission denied."

    def __init__(self, detail=None, code=None):
        super().__init__({"response": detail or self.default_detail}, code)


class IsAnonymous(BasePermission):
    """
    The custom permission class that only allow
    access if the user is NOT authenticated
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            raise CustomPermissionDenied("Already logged in, please Logout first")
        return True
