from django.db import models


class Loginadmin(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    derniere_connexion = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Administrateur'

    def __str__(self):
        return f"{self.prenom} {self.nom} (Admin)"