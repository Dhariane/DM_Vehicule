from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from vehicule.models.demandeur import Demandeur
from vehicule.models import Loginadmin
from rest_framework_simplejwt.tokens import RefreshToken
from vehicule.models import Loginadmin


def get_tokens_for_user(user):
    """Génère access + refresh token pour un utilisateur."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def connecter_utilisateur(email, password, request):
    """Authentifie un Demandeur (Utilisateur standard)."""
    # 1. Double vérification manuelle au cas où le ModelBackend de Django fait des siennes
    try:
        user = Demandeur.objects.get(email=email)
    except Demandeur.DoesNotExist:
        return None, "Identifiants invalides"

    # Vérification du mot de passe hashé
    if not check_password(password, user.password):
        return None, "Identifiants invalides"

    if not user.is_active:
        return None, "Compte désactivé"
        
    return user, None

def connecter_admin(email, password):
    """Authentifie un Administrateur (Table Loginadmin)."""
    try:
        # CORRECTION : On cherche par l'email de l'admin (pas le username) et SANS le password en clair
        admin = Loginadmin.objects.get(email=email, is_active=True)
    except Loginadmin.DoesNotExist:
        return None

    # CORRECTION : On utilise l'outil natif de Django pour comparer le hash
    if not check_password(password, admin.password):
        return None

    return admin


def register_admin(username, password, email, nom, prenom):
        if Loginadmin.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")
            
        if Loginadmin.objects.filter(email=email).exists():
            raise ValidationError("Cet email est déjà utilisé.")

        hashed_password = make_password(password)

        new_admin = Loginadmin(
            username=username,
            password=hashed_password,
            email=email,
            nom=nom,
            prenom=prenom
        )
        new_admin.save()
        
        return new_admin