from django.db import models
from django.conf import settings


class ValidationDemande(models.Model):
    DECISION_CHOICES = [
        ('approuve', 'Approuvé'),
        ('rejete', 'Rejeté'),
    ]
    ETAPE_CHOICES = [
        ('chef', 'Chef Direct'),
        ('logistique', 'Responsable Logistique'),
        ('directeur', 'Directeur'),
    ]

    demande = models.ForeignKey(
        'vehicule.DemandeVehicule',
        on_delete=models.CASCADE,
        related_name='validations'
    )
    validateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    etape = models.CharField(max_length=20, choices=ETAPE_CHOICES)
    decision = models.CharField(max_length=10, choices=DECISION_CHOICES)
    commentaire = models.TextField(blank=True)
    date_validation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_validation']

    def __str__(self):
        return f"{self.etape} → {self.decision} par {self.validateur}"