from rest_framework import permissions


class AdminOrUser(permissions.BasePermission):
    def has_permission(self, request, view):
        username = view.kwargs.get('username')
        if request.method in ('GET', 'PATCH', 'DELETE') and username == 'me':
            return True
        if request.method in ('GET', 'POST', 'PATCH', 'DELETE'):
            if (request.user.role == 'user' or request.user.role == ''
               or request.user.role == 'moderator'):
                return False
        return True


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method == 'GET'
            or request.user.is_superuser
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS\
                or obj.author == request.user\
                or request.user.role == 'moderator':
            return True
        return False
