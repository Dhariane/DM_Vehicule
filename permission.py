from rest_framework.permissions import BasePermission


class IsJWTAdmin(BasePermission):
    """Autorise uniquement l'administrateur système."""
    def has_permission(self, request, view):
        return getattr(request, 'meta_is_admin', False)


class IsJWTUser(BasePermission):
    """Autorise n'importe quel Demandeur authentifié."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and not getattr(request, 'meta_is_admin', False)
        )


class IsJWTLogistique(BasePermission):
    """Autorise les admins ET les utilisateurs avec rôle Logistique."""
    def has_permission(self, request, view):
        if getattr(request, 'meta_is_admin', False):
            return True
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'Logistique'
        )

class IsJWTAdminOrLogistique(BasePermission):
    """Autorise admin OU logistique pour toutes les méthodes."""
    def has_permission(self, request, view):
        if getattr(request, 'meta_is_admin', False):
            return True
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'Logistique'
        )