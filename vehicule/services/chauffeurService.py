from django.utils import timezone
from vehicule.models import Chauffeur


def get_all_chauffeurs():
    return Chauffeur.objects.all()


def get_chauffeurs_avec_statut():
    """Tous les chauffeurs avec statut calculé dynamiquement."""
    from vehicule.models import DemandeVehicule
    now = timezone.now()

    chauffeurs = Chauffeur.objects.filter(disponible=True)

    missions_actives = DemandeVehicule.objects.filter(
        statut='approuvee',
        date_depart__lte=now,
        date_retour__gte=now,
    ).values_list('chauffeur_id', flat=True)

    missions_futures = DemandeVehicule.objects.filter(
        statut='approuvee',
        date_depart__gt=now,
    ).values_list('chauffeur_id', flat=True)

    result = []
    for c in chauffeurs:
        if c.id in missions_actives:
            statut = 'en_mission'
        elif c.id in missions_futures:
            statut = 'reserve'
        else:
            statut = 'disponible'
        result.append({'chauffeur': c, 'statut': statut})

    return result


def get_chauffeurs_disponibles_pour(date_depart, date_retour):
    """Chauffeurs libres pour une période donnée."""
    from vehicule.models import DemandeVehicule

    chauffeurs_occupes = DemandeVehicule.objects.filter(
        statut='approuvee',
        date_depart__lt=date_retour,
        date_retour__gt=date_depart,
    ).values_list('chauffeur_id', flat=True)

    return Chauffeur.objects.filter(
        disponible=True
    ).exclude(id__in=chauffeurs_occupes)


def get_chauffeur_by_id(pk):
    try:
        return Chauffeur.objects.get(pk=pk)
    except Chauffeur.DoesNotExist:
        return None


def creer_chauffeur(data):
    return Chauffeur.objects.create(**data)


def modifier_chauffeur(chauffeur, data):
    for key, value in data.items():
        setattr(chauffeur, key, value)
    chauffeur.save()
    return chauffeur


def desactiver_chauffeur(chauffeur):
    chauffeur.disponible = False
    chauffeur.save(update_fields=['disponible'])
    return chauffeur