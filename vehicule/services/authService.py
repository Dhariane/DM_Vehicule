from xml.dom import ValidationErr

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from vehicule.models.demandeur import Demandeur
from vehicule.models import Loginadmin
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
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import jwt
from django.conf import settings

def is_admin(request):
    auth_header = request.headers.get('Authorization', '')
    print(">>> AUTH HEADER:", auth_header)
    
    if not auth_header.startswith('Bearer '):
        print(">>> PAS DE BEARER TOKEN")
        return False
    
    token_str = auth_header.split(' ')[1]
    print(">>> TOKEN:", token_str[:50], "...")
    
    try:
        import jwt
        from django.conf import settings
        payload = jwt.decode(token_str, settings.SECRET_KEY, algorithms=['HS256'])
        print(">>> PAYLOAD:", payload)
        print(">>> TYPE:", payload.get('type'))
        return payload.get('type') == 'admin'
    except Exception as e:
        print(">>> ERREUR JWT:", e)
        return False