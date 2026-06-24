import secrets
import string
from vehicule.models import Demandeur
from vehicule.services.emailService import envoyer_email_credentials


def generer_mot_de_passe():
    """Génère un mot de passe sécurisé de 10 caractères."""
    alphabet = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(secrets.choice(alphabet) for _ in range(10))


def get_all_demandeurs():
    return Demandeur.objects.select_related('chef_direct').all()


def get_demandeur_by_id(pk):
    try:
        return Demandeur.objects.select_related('chef_direct').get(pk=pk)
    except Demandeur.DoesNotExist:
        return None


def creer_demandeur(data):
    password = data.pop('password', None)

    # Si pas de mot de passe fourni → générer automatiquement
    if not password:
        password = generer_mot_de_passe()

    user = Demandeur(**data)
    user.set_password(password)
    user.save()

    # Envoyer les credentials par email
    if user.email:
        envoyer_email_credentials(user, password)

    return user


def modifier_demandeur(user, data):
    for key, value in data.items():
        setattr(user, key, value)
    user.save()
    return user


def desactiver_demandeur(user):
    user.is_active = False
    user.save(update_fields=['is_active'])
    return user


def reinitialiser_mot_de_passe(user):
    """Réinitialise et renvoie un nouveau mot de passe par email."""
    password = generer_mot_de_passe()
    user.set_password(password)
    user.save(update_fields=['password'])
    if user.email:
        envoyer_email_credentials(user, password)
    return user