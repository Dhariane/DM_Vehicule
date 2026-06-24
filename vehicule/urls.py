from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from vehicule.controllers.authControllers import (
    LoginController, LogoutController, MeController,
    LoginAdminController, LogoutAdminController, MeAdminController,
)
from vehicule.controllers.adminControllers import (
    AdminStatsController,
    AdminDemandeurListCreateController,
    AdminDemandeurDetailController,
    AdminVehiculeListCreateController,
    AdminVehiculeDetailController,
    AdminChauffeurListCreateController,
    AdminChauffeurDetailController,
)
from vehicule.controllers.demandeControllers import (
    MesDemandesController,
    DetailDemandeController,
)
from vehicule.controllers.validationControllers import (
    ValidationListController,
    ValidationActionController,
    TerminerMissionController,       # ← ajouter
)
from vehicule.controllers.chauffeurControllers import (
    ChauffeurListCreateController,
    ChauffeurDetailController,
)
from vehicule.controllers.vehiculeControllers import (
    VehiculeListCreateController,
    VehiculeDetailController,        # ← décommenter l'import
    VehiculeDisponibleController,
    MissionsEnCoursController,
)
from vehicule.controllers.financementControllers import (
    FinancementListCreateController,
    FinancementDetailController,
)

urlpatterns = [
    # ── Auth utilisateur JWT ──────────────────────────
    path('auth/login/',           LoginController.as_view()),
    path('auth/logout/',          LogoutController.as_view()),
    path('auth/me/',              MeController.as_view()),
    path('auth/token/refresh/',   TokenRefreshView.as_view()),

    # ── Auth admin ────────────────────────────────────
    path('auth/admin/login/',     LoginAdminController.as_view()),
    path('auth/admin/logout/',    LogoutAdminController.as_view()),
    path('auth/admin/me/',        MeAdminController.as_view()),

    # ── Routes ADMIN ──────────────────────────────────
    path('admin/stats/',                      AdminStatsController.as_view()),
    path('admin/demandeurs/',                 AdminDemandeurListCreateController.as_view()),
    path('admin/demandeurs/<int:pk>/',        AdminDemandeurDetailController.as_view()),
    path('admin/vehicules/',                  AdminVehiculeListCreateController.as_view()),
    path('admin/vehicules/<int:pk>/',         AdminVehiculeDetailController.as_view()),
    path('admin/chauffeurs/',                 AdminChauffeurListCreateController.as_view()),
    path('admin/chauffeurs/<int:pk>/',        AdminChauffeurDetailController.as_view()),

    # ── Routes UTILISATEUR/LOGISTIQUE ─────────────────
    path('demandes/',                         MesDemandesController.as_view()),
    path('demandes/<int:pk>/',                DetailDemandeController.as_view()),
    path('demandes/<int:pk>/terminer/',       TerminerMissionController.as_view()),  # ← nouveau
    path('validations/',                      ValidationListController.as_view()),
    path('validations/<int:pk>/',             ValidationActionController.as_view()),

    # ✅ Véhicules — ordre important : spécifique avant générique
    path('vehicules/disponibles/',            VehiculeDisponibleController.as_view()),
    path('vehicules/',                        VehiculeListCreateController.as_view()),
    path('vehicules/<int:pk>/',               VehiculeDetailController.as_view()),  # ← décommenté

    # ✅ Chauffeurs
    path('chauffeurs/',                       ChauffeurListCreateController.as_view()),
    path('chauffeurs/<int:pk>/',              ChauffeurDetailController.as_view()),

    # ── Financements ──────────────────────────────────
    path('financements/',                     FinancementListCreateController.as_view()),
    path('financements/<int:pk>/',            FinancementDetailController.as_view()),

    # ── Missions ──────────────────────────────────────
    path('missions/en-cours/',                MissionsEnCoursController.as_view()),
]