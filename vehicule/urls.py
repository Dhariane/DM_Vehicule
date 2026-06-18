from django.urls import path
from vehicule.controllers import (
    LoginController, LogoutController, MeController,
    LoginAdminController, LogoutAdminController, MeAdminController,
    DemandeurListCreateController, DemandeurDetailController,
    ChauffeurListCreateController, ChauffeurDetailController,
    VehiculeListCreateController, VehiculeDetailController,
    MesDemandesController, DetailDemandeController,
    ValidationListController, ValidationActionController,
)

urlpatterns = [
    # Auth utilisateur
    path('auth/login/', LoginController.as_view()),
    path('auth/logout/', LogoutController.as_view()),
    path('auth/me/', MeController.as_view()),

    # Auth admin
    path('auth/admin/login/', LoginAdminController.as_view()),
    path('auth/admin/logout/', LogoutAdminController.as_view()),
    path('auth/admin/me/', MeAdminController.as_view()),

    # Demandeurs
    path('demandeurs/', DemandeurListCreateController.as_view()),
    path('demandeurs/<int:pk>/', DemandeurDetailController.as_view()),

    # Chauffeurs
    path('chauffeurs/', ChauffeurListCreateController.as_view()),
    path('chauffeurs/<int:pk>/', ChauffeurDetailController.as_view()),

    # Véhicules
    path('vehicules/', VehiculeListCreateController.as_view()),
    path('vehicules/<int:pk>/', VehiculeDetailController.as_view()),

    # Demandes
    path('demandes/', MesDemandesController.as_view()),
    path('demandes/<int:pk>/', DetailDemandeController.as_view()),

    # Validations
    path('validations/', ValidationListController.as_view()),
    path('validations/<int:pk>/', ValidationActionController.as_view()),
]