from .authControllers import (
    LoginController,
    LogoutController,
    MeController,
    LoginAdminController,
    LogoutAdminController,
    MeAdminController,
)
from .adminControllers import (
    AdminStatsController,
    AdminDemandeurListCreateController,
    AdminDemandeurDetailController,
    AdminVehiculeListCreateController,
    AdminVehiculeDetailController,
    AdminChauffeurListCreateController,
    AdminChauffeurDetailController,
)
from .demandeControllers import (
    MesDemandesController,
    DetailDemandeController,
)
from .validationControllers import (
    ValidationListController,
    ValidationActionController,
)
from .chauffeurControllers import (
    ChauffeurListCreateController,
    ChauffeurDetailController,
)
from .vehiculeControllers import (
    VehiculeListCreateController,
    VehiculeDetailController,
)
from .financementControllers import (  # ← nouveau
    FinancementListCreateController,
    FinancementDetailController,
)