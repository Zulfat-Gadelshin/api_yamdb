from rest_framework import permissions


class AdminOrUser(permissions.BasePermission):
    def has_permission(self, request, view):
        username = view.kwargs.get('username')
        if request.method in ('GET', 'PATCH', 'DELETE') and username == 'me':
            return True
        if request.method in ('GET', 'POST', 'PATCH', 'DELETE'):
            if (request.user.role == 'user' or request.user.role == '' or
                    request.user.role == 'moderator'):
                return False
        return True
