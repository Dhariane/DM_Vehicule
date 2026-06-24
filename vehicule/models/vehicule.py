from datetime import timezone

from django.db import models


class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=20, unique=True)
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    disponible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Véhicule'
        ordering = ['marque', 'modele']


    def est_disponible_pour(self, date_depart, date_retour):
        """Vérifie si le véhicule est libre pour cette période."""
        from vehicule.models.demande import DemandeVehicule
        conflit = DemandeVehicule.objects.filter(
            vehicule=self,
            statut='approuvee',
            date_depart__lt=date_retour,
            date_retour__gt=date_depart,
        ).exists()
        return not conflit

    def est_en_mission(self):
        """Vérifie si le véhicule est actuellement en mission."""
        from vehicule.models.demande import DemandeVehicule
        now = timezone.now()
        return DemandeVehicule.objects.filter(
            vehicule=self,
            statut='approuvee',
            date_depart__lte=now,
            date_retour__gte=now,
        ).exists()

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.immatriculation})"
    
    