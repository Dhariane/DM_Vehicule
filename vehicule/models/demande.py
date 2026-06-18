from django.db import models
from django.conf import settings


class DemandeVehicule(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('rejetee', 'Rejetée'),
    ]
    ETAPE_CHOICES = [
        ('chef', 'Chef Direct'),
        ('logistique', 'Responsable Logistique'),
        ('directeur', 'Directeur'),
        ('termine', 'Terminé'),
    ]
    MOTIF_CHOICES = [
        ('mission', 'Mission terrain'),
        ('transport', 'Transport de matériel'),
        ('deplacement', 'Déplacement officiel'),
        ('autre', 'Autre'),
    ]

    demandeur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='demandes_vehicule'
    )
    vehicule = models.ForeignKey(
        'vehicule.Vehicule',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='demandes'
    )
    chauffeur = models.ForeignKey(
        'vehicule.Chauffeur',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='missions'
    )
    motif = models.CharField(max_length=20, choices=MOTIF_CHOICES)
    destination = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_depart = models.DateTimeField()
    date_retour = models.DateTimeField()
    nombre_passagers = models.IntegerField(default=1)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    etape_validation = models.CharField(max_length=20, choices=ETAPE_CHOICES, default='chef')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Demande de véhicule'
        ordering = ['-date_creation']

    def __str__(self):
        return f"#{self.pk} {self.demandeur} → {self.destination}"