from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow staff users to edit it. 
    Read permissions are allowed to any request, so GET, HEAD or OPTIONS requests are allowed.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the staff users.
        return request.user and request.user.is_staff
