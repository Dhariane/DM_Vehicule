from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from vehicule.models import Loginadmin


def get_tokens_for_user(user):
    """Génère access + refresh token pour un utilisateur."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def connecter_utilisateur(username, password, request):
    user = authenticate(request, username=username, password=password)
    if not user:
        return None, "Identifiants invalides"
    if not user.is_active:
        return None, "Compte désactivé"
    return user, None


def connecter_admin(username, password):
    try:
        admin = Loginadmin.objects.get(username=username, is_active=True)
    except Loginadmin.DoesNotExist:
        return None

    if not check_password(password, admin.password):
        return None

    admin.derniere_connexion = timezone.now()
    admin.save(update_fields=['derniere_connexion'])
    return admin


def get_admin_session(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return None
    try:
        return Loginadmin.objects.get(pk=admin_id, is_active=True)
    except Loginadmin.DoesNotExist:
        return None


def is_admin(request):
    return get_admin_session(request) is not None