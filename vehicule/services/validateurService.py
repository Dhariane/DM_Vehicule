from vehicule.models import ValidationDemande


def get_validations_by_demande(demande_id):
    return ValidationDemande.objects.filter(
        demande_id=demande_id
    ).select_related('validateur')


def creer_validation(demande, validateur, etape, decision, commentaire=''):
    return ValidationDemande.objects.create(
        demande=demande,
        validateur=validateur,
        etape=etape,
        decision=decision,
        commentaire=commentaire,
    )