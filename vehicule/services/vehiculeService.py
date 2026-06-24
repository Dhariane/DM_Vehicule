from django.utils import timezone
from vehicule.models import Vehicule


def get_all_vehicules():
    return Vehicule.objects.all()


def get_vehicules_disponibles():
    """Retourne tous les véhicules disponibles maintenant."""
    return Vehicule.objects.filter(disponible=True)


def get_vehicules_disponibles_pour(date_depart, date_retour):
    """Retourne les véhicules libres pour une période donnée."""
    from vehicule.models import DemandeVehicule
    vehicules_occupes = DemandeVehicule.objects.filter(
        statut='approuvee',
        date_depart__lt=date_retour,
        date_retour__gt=date_depart,
    ).values_list('vehicule_id', flat=True)

    return Vehicule.objects.filter(
        disponible=True
    ).exclude(id__in=vehicules_occupes)


def get_vehicules_en_mission():
    """Retourne les véhicules actuellement en mission."""
    from vehicule.models import DemandeVehicule
    now = timezone.now()
    demandes_actives = DemandeVehicule.objects.filter(
        statut='approuvee',
        date_depart__lte=now,
        date_retour__gte=now,
    ).select_related('vehicule', 'chauffeur', 'demandeur')
    return demandes_actives


def get_vehicule_by_id(pk):
    try:
        return Vehicule.objects.get(pk=pk)
    except Vehicule.DoesNotExist:
        return None


def creer_vehicule(data):
    return Vehicule.objects.create(**data)


def modifier_vehicule(vehicule, data):
    for key, value in data.items():
        setattr(vehicule, key, value)
    vehicule.save()
    return vehicule


def desactiver_vehicule(vehicule):
    vehicule.disponible = False
    vehicule.save(update_fields=['disponible'])
    return vehicule