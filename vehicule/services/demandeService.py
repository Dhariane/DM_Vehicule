from django.utils import timezone
from django.db import transaction
from vehicule.models import DemandeVehicule
from vehicule.services.validateurService import creer_validation
from vehicule.services.chauffeurService import get_chauffeur_by_id
from vehicule.services.vehiculeService import get_vehicule_by_id
from vehicule.services.emailService import (
    envoyer_email_chef,
    envoyer_email_decision,
    envoyer_email_approbation_finale,
    envoyer_email_logistique
)

ETAPES = ['chef', 'logistique', 'directeur', 'termine']


def _etape_suivante(etape):
    try:
        return ETAPES[ETAPES.index(etape) + 1]
    except (ValueError, IndexError):
        return 'termine'


def get_mes_demandes(user):
    return DemandeVehicule.objects.filter(
        demandeur=user
    ).select_related('vehicule', 'chauffeur').prefetch_related('validations')


def get_demande_by_id(pk, user):
    try:
        return DemandeVehicule.objects.prefetch_related(
            'validations'
        ).get(pk=pk, demandeur=user)
    except DemandeVehicule.DoesNotExist:
        return None


def creer_demande(demandeur, data):
    if data['date_depart'] <= timezone.now():
        raise ValueError("La date de départ doit être dans le futur.")

    if data['date_retour'] <= data['date_depart']:
        raise ValueError("La date de retour doit être après le départ.")

    # ✅ Si pas de chef direct → passer directement au logistique
    if demandeur.chef_direct:
        etape_initiale = 'chef'
    else:
        etape_initiale = 'logistique'

    demande = DemandeVehicule.objects.create(
        demandeur=demandeur,
        motif=data['motif'],
        destination=data['destination'],
        description=data.get('description', ''),
        date_depart=data['date_depart'],
        date_retour=data['date_retour'],
        nombre_passagers=data.get('nombre_passagers', 1),
        etape_validation=etape_initiale,
        statut='en_attente',
    )

    # ✅ Envoyer l'email selon l'étape
    if etape_initiale == 'chef':
        envoyer_email_chef(demande)
    else:
        envoyer_email_logistique(demande)  # ← à créer dans emailService.py

    return demande


def annuler_demande(demande):
    if demande.statut != 'en_attente':
        raise ValueError("Seules les demandes en attente peuvent être annulées.")
    demande.delete()


def _verifier_droit_validation(demande, validateur):
    etape = demande.etape_validation

    if etape == 'chef':
        if demande.demandeur.chef_direct != validateur:
            raise ValueError("Vous n'êtes pas le chef direct de ce demandeur.")

    elif etape == 'logistique':
        if validateur.role != 'Logistique':
            raise ValueError("Vous n'avez pas le rôle Logistique.")

    elif etape == 'directeur':
        if validateur.role != 'Directeur':
            raise ValueError("Vous n'avez pas le rôle Directeur.")


@transaction.atomic
def traiter_validation(demande, validateur, decision,
                       commentaire='', vehicule_id=None, chauffeur_id=None):

    if demande.statut in ('approuvee', 'rejetee'):
        raise ValueError("Cette demande est déjà clôturée.")

    _verifier_droit_validation(demande, validateur)

    etape_courante = demande.etape_validation
    creer_validation(demande, validateur, etape_courante, decision, commentaire)

    if decision == 'rejete':
        demande.statut = 'rejetee'
        demande.save(update_fields=['statut', 'date_modification'])
        envoyer_email_decision(demande, etape_courante, 'rejete', commentaire)
        return demande

    if etape_courante == 'logistique':
        if vehicule_id:
            vehicule = get_vehicule_by_id(vehicule_id)
            if not vehicule:
                raise ValueError("Véhicule introuvable.")
            # Vérifier disponibilité sur la période
            if not vehicule.est_disponible_pour(demande.date_depart, demande.date_retour):
                raise ValueError("Ce véhicule est déjà réservé sur cette période.")
            demande.vehicule = vehicule

        if chauffeur_id:
            chauffeur = get_chauffeur_by_id(chauffeur_id)
            if not chauffeur:
                raise ValueError("Chauffeur introuvable.")
            # Vérifier disponibilité sur la période
            if not chauffeur.est_disponible_pour(demande.date_depart, demande.date_retour):
                raise ValueError("Ce chauffeur est déjà assigné sur cette période.")
            demande.chauffeur = chauffeur

    prochaine = _etape_suivante(etape_courante)

    if prochaine == 'termine':
        demande.statut = 'approuvee'
        demande.etape_validation = 'termine'
        # ← Plus de disponible=False ici !
        # La disponibilité est calculée dynamiquement via est_disponible_pour()
        demande.save(update_fields=[
            'statut', 'etape_validation',
            'vehicule', 'chauffeur', 'date_modification',
        ])
        envoyer_email_approbation_finale(demande)
    else:
        demande.etape_validation = prochaine
        demande.save(update_fields=[
            'etape_validation', 'vehicule',
            'chauffeur', 'date_modification',
        ])
        envoyer_email_decision(demande, etape_courante, 'approuve', commentaire)

    return demande

def demandes_a_valider(user):
    role = user.role

    if role == 'Chef':
        return DemandeVehicule.objects.filter(
            statut='en_attente',
            etape_validation='chef',
            demandeur__chef_direct=user,
        ).select_related('demandeur', 'vehicule', 'chauffeur').prefetch_related('validations')

    if role == 'Logistique':
        return DemandeVehicule.objects.filter(
            statut='en_attente',
            etape_validation='logistique',
        ).select_related('demandeur', 'vehicule', 'chauffeur').prefetch_related('validations')

    if role == 'Directeur':
        return DemandeVehicule.objects.filter(
            statut='en_attente',
            etape_validation='directeur',
        ).select_related('demandeur', 'vehicule', 'chauffeur').prefetch_related('validations')

    return DemandeVehicule.objects.none()