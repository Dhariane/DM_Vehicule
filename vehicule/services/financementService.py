from vehicule.models.financement import Financement


def get_all_financements():
    return Financement.objects.all()


def get_financement_by_id(pk):
    try:
        return Financement.objects.get(pk=pk)
    except Financement.DoesNotExist:
        return None


def creer_financement(data):
    return Financement.objects.create(**data)


def modifier_financement(financement, data):
    for key, value in data.items():
        setattr(financement, key, value)
    financement.save()
    return financement


def supprimer_financement(financement):
    financement.delete()