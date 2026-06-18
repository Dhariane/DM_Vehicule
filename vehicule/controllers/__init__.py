from .authControllers import (
    LoginController,
    LogoutController,
    MeController,
    LoginAdminController,
    LogoutAdminController,
    MeAdminController,
    RegisterAdminController,
)
from .demandeurControllers import (
    DemandeurListCreateController,
    DemandeurDetailController,
)
from .chauffeurControllers import (
    ChauffeurListCreateController,
    ChauffeurDetailController,
)
from .vehiculeControllers import (
    VehiculeListCreateController,
    VehiculeDetailController,
)
from .demandeControllers import (       # ← était demandeurControllers, c'est faux
    MesDemandesController,
    DetailDemandeController,
)
from .validationControllers import (
    ValidationListController,
    ValidationActionController,
)