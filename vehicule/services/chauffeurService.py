from vehicule.models import Chauffeur


def get_all_chauffeurs():
    return Chauffeur.objects.filter(disponible=True)


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