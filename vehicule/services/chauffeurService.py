from vehicule.models import Chauffeur


def get_all_chauffeurs():
    return Chauffeur.objects.filter(disponible=True)


def get_chauffeur_by_id(pk):
    try:
        return Chauffeur.objects.get(pk=pk)
    except Chauffeur.DoesNotExist:
        return None


from vehicule.models import Chauffeur

def creer_chauffeur(nom, prenom, telephone, email="", financement=None):
    return Chauffeur.objects.create(
        nom=nom,
        prenom=prenom,
        telephone=telephone,
        email=email,
        financement=financement
    )

def modifier_chauffeur(instance, validated_data):
    instance.nom = validated_data.get('nom', instance.nom)
    instance.prenom = validated_data.get('prenom', instance.prenom)
    instance.telephone = validated_data.get('telephone', instance.telephone)
    instance.email = validated_data.get('email', instance.email)
    instance.disponible = validated_data.get('disponible', instance.disponible)
    
    # Gère la modification ou la suppression du financement lié
    if 'financement' in validated_data:
        instance.financement = validated_data['financement']
        
    instance.save()
    return instance


def desactiver_chauffeur(chauffeur):
    chauffeur.disponible = False
    chauffeur.save(update_fields=['disponible'])
    return chauffeur