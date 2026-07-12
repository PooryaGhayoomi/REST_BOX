from rest_framework.permissions import BasePermission


class IsHost(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "HOST"
        )