from rest_framework import permissions

class IsAuthenticatedSU(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        if request.user.is_authenticated() and len(request.user._suadrole) > 0:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated() and len(request.user._suadrole) > 0:
            return True

        return False
