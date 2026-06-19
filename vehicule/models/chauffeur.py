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

    def __str__(self):
        return f"{self.prenom} {self.nom}"