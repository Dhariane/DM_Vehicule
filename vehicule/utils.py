from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import BasePermission


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class IsAdminSession(BasePermission):
    """Permission pour le Loginadmin via session."""
    def has_permission(self, request, view):
        return request.session.get('admin_id') is not None


class IsAuthenticatedOrAdminSession(BasePermission):
    """JWT user OU admin session."""
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        if request.session.get('admin_id'):
            return True
        return False