from rest_framework.permissions import BasePermission

class IsJWTAdmin(BasePermission):
    """Autorise uniquement l'administrateur système."""
    def has_permission(self, request, view):
        # On vérifie le flag injecté par HybridJWTAuthentication
        return getattr(request, 'meta_is_admin', False)

class IsJWTUser(BasePermission):
    """Autorise n'importe quel Demandeur authentifié."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not getattr(request, 'meta_is_admin', False)