from rest_framework.permissions import BasePermission

class IsAnonymousUser(BasePermission):
    """
    Allows access only to non-authenticated users (users who are not logged in).
    """
    def has_permission(self, request, view):
        return not request.user.is_authenticated