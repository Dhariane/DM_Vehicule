from django.db import models


class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=20, unique=True)
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    capacite = models.IntegerField(help_text="Nombre de places")
    disponible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Véhicule'
        ordering = ['marque', 'modele']

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.immatriculation})"