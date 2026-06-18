from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from vehicule.models import Loginadmin


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