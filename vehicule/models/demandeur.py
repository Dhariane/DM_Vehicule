from django.contrib.auth.models import AbstractUser
from django.db import models
from vehicule.models.financement import Financement


class Demandeur(AbstractUser):
    ROLE_CHOICES = [
        ('Demandeur', 'Demandeur'),
        ('Chef', 'Chef Direct'),
        ('Logistique', 'Responsable Logistique'),
        ('Directeur', 'Directeur'),
    ]
    email = models.EmailField(unique=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Demandeur')

    telephone = models.CharField(max_length=20, blank=True)

    service = models.CharField(max_length=100, blank=True)

    poste = models.CharField(max_length=100, blank=True)

    financement = models.ForeignKey(
        Financement,                            
        on_delete=models.SET_NULL, null=True, blank=True)
    
    chef_direct = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='subordonnes',
        limit_choices_to={'role': 'Chef'},
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_email_chef(self):
        if self.chef_direct and self.chef_direct.email:
            return self.chef_direct.email
        return None

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"