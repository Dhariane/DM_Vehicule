from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from vehicule.models import Demandeur, Vehicule, Chauffeur
from vehicule.models import DemandeVehicule
from vehicule.dto import (
    DemandeurSerializer,
    CreerDemandeurSerializer,
    UpdateDemandeurSerializer,
    VehiculeSerializer,
    CreerVehiculeSerializer,
    ChauffeurSerializer,
    CreerChauffeurSerializer,
)
from vehicule.services import (
    is_admin,
    get_all_demandeurs,
    get_demandeur_by_id,
    creer_demandeur,
    modifier_demandeur,
    desactiver_demandeur,
    get_all_vehicules,
    get_vehicule_by_id,
    creer_vehicule,
    modifier_vehicule,
    desactiver_vehicule,
    get_all_chauffeurs,
    get_chauffeur_by_id,
    creer_chauffeur,
    modifier_chauffeur,
    desactiver_chauffeur,
)


def check_admin(request):
    if not is_admin(request):
        return Response({'error': 'Accès réservé à l\'admin'}, status=403)
    return None


# ── Stats dashboard admin ────────────────────────────────────

class AdminStatsController(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        err = check_admin(request)
        if err:
            return err
        return Response({
            'total_demandeurs': Demandeur.objects.count(),
            'total_vehicules': Vehicule.objects.count(),
            'total_chauffeurs': Chauffeur.objects.count(),
            'total_demandes': DemandeVehicule.objects.count(),
            'demandes_en_attente': DemandeVehicule.objects.filter(statut='en_attente').count(),
            'demandes_approuvees': DemandeVehicule.objects.filter(statut='approuvee').count(),
            'demandes_rejetees': DemandeVehicule.objects.filter(statut='rejetee').count(),
        })


# ── Demandeurs ───────────────────────────────────────────────

class AdminDemandeurListCreateController(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        err = check_admin(request)
        if err:
            return err
        users = get_all_demandeurs()
        return Response(DemandeurSerializer(users, many=True).data)

    def post(self, request):
        err = check_admin(request)
        if err:
            return err
        ser = CreerDemandeurSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        user = ser.save()
        return Response(DemandeurSerializer(user).data, status=201)


class AdminDemandeurDetailController(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        err = check_admin(request)
        if err:
            return err
        user = get_demandeur_by_id(pk)
        if not user:
            return Response({'error': 'Introuvable'}, status=404)
        return Response(DemandeurSerializer(user).data)

    def put(self, request, pk):
        err = check_admin(request)
        if err:
            return err
        user = get_demandeur_by_id(pk)
        if not user:
            return Response({'error': 'Introuvable'}, status=404)
        ser = UpdateDemandeurSerializer(user, data=request.data, partial=True)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        user = modifier_demandeur(user, ser.validated_data)
        return Response(DemandeurSerializer(user).data)

    def delete(self, request, pk):
        err = check_admin(request)
        if err:
            return err
        user = get_demandeur_by_id(pk)
        if not user:
            return Response({'error': 'Introuvable'}, status=404)
        desactiver_demandeur(user)
        return Response(status=204)


# ── Véhicules ────────────────────────────────────────────────

class AdminVehiculeListCreateController(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        err = check_admin(request)
        if err:
            return err
        vehicules = Vehicule.objects.all()
        return Response(VehiculeSerializer(vehicules, many=True).data)

    def post(self, request):
        err = check_admin(request)
        if err:
            return err
        ser = CreerVehiculeSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        vehicule = ser.save()
        return Response(VehiculeSerializer(vehicule).data, status=201)


class AdminVehiculeDetailController(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        err = check_admin(request)
        if err:
            return err
        vehicule = get_vehicule_by_id(pk)
        if not vehicule:
            return Response({'error': 'Introuvable'}, status=404)
        return Response(VehiculeSerializer(vehicule).data)

    def put(self, request, pk):
        err = check_admin(request)
        if err:
            return err
        vehicule = get_vehicule_by_id(pk)
        if not vehicule:
            return Response({'error': 'Introuvable'}, status=404)
        ser = VehiculeSerializer(vehicule, data=request.data, partial=True)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        vehicule = modifier_vehicule(vehicule, ser.validated_data)
        return Response(VehiculeSerializer(vehicule).data)

    def delete(self, request, pk):
        err = check_admin(request)
        if err:
            return err
        vehicule = get_vehicule_by_id(pk)
        if not vehicule:
            return Response({'error': 'Introuvable'}, status=404)
        desactiver_vehicule(vehicule)
        return Response(status=204)


# ── Chauffeurs ───────────────────────────────────────────────

class AdminChauffeurListCreateController(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        err = check_admin(request)
        if err:
            return err
        chauffeurs = Chauffeur.objects.all()
        return Response(ChauffeurSerializer(chauffeurs, many=True).data)

    def post(self, request):
        err = check_admin(request)
        if err:
            return err
        ser = CreerChauffeurSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        chauffeur = ser.save()
        return Response(ChauffeurSerializer(chauffeur).data, status=201)


class AdminChauffeurDetailController(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        err = check_admin(request)
        if err:
            return err
        chauffeur = get_chauffeur_by_id(pk)
        if not chauffeur:
            return Response({'error': 'Introuvable'}, status=404)
        return Response(ChauffeurSerializer(chauffeur).data)

    def put(self, request, pk):
        err = check_admin(request)
        if err:
            return err
        chauffeur = get_chauffeur_by_id(pk)
        if not chauffeur:
            return Response({'error': 'Introuvable'}, status=404)
        ser = ChauffeurSerializer(chauffeur, data=request.data, partial=True)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        chauffeur = modifier_chauffeur(chauffeur, ser.validated_data)
        return Response(ChauffeurSerializer(chauffeur).data)

    def delete(self, request, pk):
        err = check_admin(request)
        if err:
            return err
        chauffeur = get_chauffeur_by_id(pk)
        if not chauffeur:
            return Response({'error': 'Introuvable'}, status=404)
        desactiver_chauffeur(chauffeur)
        return Response(status=204)