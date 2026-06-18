from django.contrib.auth.hashers import check_password
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