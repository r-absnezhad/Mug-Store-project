from rest_framework.permissions import BasePermission


class IsAuthenticatedOrAdmin(BasePermission):
    """
    Allow authenticated users to create, but restrict other actions to admin users.
    """
    def has_permission(self, request, view):
        if view.action == "create" or request.method == "POST":
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff