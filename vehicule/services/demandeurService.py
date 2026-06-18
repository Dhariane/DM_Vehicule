from vehicule.models import Demandeur


def get_all_demandeurs():
    return Demandeur.objects.select_related('chef_direct').all()


def get_demandeur_by_id(pk):
    try:
        return Demandeur.objects.select_related('chef_direct').get(pk=pk)
    except Demandeur.DoesNotExist:
        return None


def creer_demandeur(data):
    password = data.pop('password')
    user = Demandeur(**data)
    user.set_password(password)
    user.save()
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