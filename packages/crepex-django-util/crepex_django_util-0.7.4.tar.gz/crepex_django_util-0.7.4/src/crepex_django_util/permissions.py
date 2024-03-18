from rest_framework.permissions import BasePermission


class IsNotAuthenticated(BasePermission):
    """
    비회원 전용
    """

    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)
