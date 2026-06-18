from vehicule.models import Vehicule


def get_all_vehicules():
    return Vehicule.objects.filter(disponible=True)


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