from rest_framework import permissions

from core.exceptions import GenericException


class isAuthenticated(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        raise GenericException(
            {"message": "Authentication credentials were not provided."}
        )


class AllowAny(permissions.AllowAny):

    def has_permission(self, request, view):
        return True
