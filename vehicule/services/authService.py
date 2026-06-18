from xml.dom import ValidationErr

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from vehicule.models import Demandeur, Loginadmin


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


from django.contrib.auth import get_user_model

def connecter_utilisateur(email, password):
    User = get_user_model()
    try:
        # 1. On cherche l'utilisateur dans la base de données grâce à son email
        user = User.objects.get(email=email)
        
        # 2. On vérifie si le mot de passe est correct et si le compte est actif
        if user.check_password(password) and user.is_active:
            return user, None
        else:
            return None, "Identifiants invalides"
            
    except User.DoesNotExist:
        # Si aucun utilisateur n'a cet email
        return None, "Identifiants invalides"


def connecter_admin(email, password):
    try:
        admin = Loginadmin.objects.get(email=email, is_active=True)
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

def register_admin(username, password, email, nom, prenom):
        if Loginadmin.objects.filter(username=username).exists():
            raise ValidationErr("Ce nom d'utilisateur est déjà pris.")
            
        if Loginadmin.objects.filter(email=email).exists():
            raise ValidationErr("Cet email est déjà utilisé.")

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