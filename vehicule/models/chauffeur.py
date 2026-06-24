from datetime import timezone

from django.db import models
from vehicule.models.financement import Financement  # Assure-toi d'importer le modèle

class Chauffeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    # Nouvelle relation
    financement = models.ForeignKey(
        Financement, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='chauffeurs'
    )

    class Meta:
        verbose_name = 'Chauffeur'
        ordering = ['nom', 'prenom']


    def est_disponible_pour(self, date_depart, date_retour):
        """Vérifie si le chauffeur est libre pour cette période."""
        from vehicule.models.demande import DemandeVehicule
        conflit = DemandeVehicule.objects.filter(
            chauffeur=self,
            statut='approuvee',
            date_depart__lt=date_retour,
            date_retour__gt=date_depart,
        ).exists()
        return not conflit

    def est_en_mission(self):
        """Vérifie si le chauffeur est actuellement en mission."""
        from vehicule.models.demande import DemandeVehicule
        now = timezone.now()
        return DemandeVehicule.objects.filter(
            chauffeur=self,
            statut='approuvee',
            date_depart__lte=now,
            date_retour__gte=now,
        ).exists()
    def __str__(self):
        return f"{self.prenom} {self.nom}"