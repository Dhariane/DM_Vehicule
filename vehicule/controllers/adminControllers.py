from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from vehicule.models import Demandeur, Vehicule
from vehicule.serializers import (
    DemandeurSerializer,
    CreerDemandeurSerializer,
    UpdateDemandeurSerializer,
    VehiculeSerializer,
    CreerVehiculeSerializer,
)
from vehicule.utils import IsAdminSession
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
)


class UtilisateurListCreateController(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if not is_admin(request):
            return Response({'error': 'Accès réservé à l\'admin'}, status=403)
        users = get_all_demandeurs()
        return Response(DemandeurSerializer(users, many=True).data)

    def post(self, request):
        if not is_admin(request):
            return Response({'error': 'Accès réservé à l\'admin'}, status=403)
        ser = CreerDemandeurSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        user = ser.save()
        return Response(DemandeurSerializer(user).data, status=201)


class UtilisateurDetailController(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        if not is_admin(request):
            return Response({'error': 'Accès réservé'}, status=403)
        user = get_demandeur_by_id(pk)
        if not user:
            return Response({'error': 'Introuvable'}, status=404)
        return Response(DemandeurSerializer(user).data)

    def put(self, request, pk):
        if not is_admin(request):
            return Response({'error': 'Accès réservé'}, status=403)
        user = get_demandeur_by_id(pk)
        if not user:
            return Response({'error': 'Introuvable'}, status=404)
        ser = UpdateDemandeurSerializer(user, data=request.data, partial=True)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        user = modifier_demandeur(user, ser.validated_data)
        return Response(DemandeurSerializer(user).data)

    def delete(self, request, pk):
        if not is_admin(request):
            return Response({'error': 'Accès réservé'}, status=403)
        user = get_demandeur_by_id(pk)
        if not user:
            return Response({'error': 'Introuvable'}, status=404)
        desactiver_demandeur(user)
        return Response(status=204)


class VehiculeListCreateController(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        vehicules = get_all_vehicules()
        return Response(VehiculeSerializer(vehicules, many=True).data)

    def post(self, request):
        if not is_admin(request):
            return Response({'error': 'Accès réservé'}, status=403)
        ser = CreerVehiculeSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        vehicule = ser.save()
        return Response(VehiculeSerializer(vehicule).data, status=201)


class VehiculeDetailController(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        vehicule = get_vehicule_by_id(pk)
        if not vehicule:
            return Response({'error': 'Introuvable'}, status=404)
        return Response(VehiculeSerializer(vehicule).data)

    def put(self, request, pk):
        if not is_admin(request):
            return Response({'error': 'Accès réservé'}, status=403)
        vehicule = get_vehicule_by_id(pk)
        if not vehicule:
            return Response({'error': 'Introuvable'}, status=404)
        ser = VehiculeSerializer(vehicule, data=request.data, partial=True)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        vehicule = modifier_vehicule(vehicule, ser.validated_data)
        return Response(VehiculeSerializer(vehicule).data)

    def delete(self, request, pk):
        if not is_admin(request):
            return Response({'error': 'Accès réservé'}, status=403)
        vehicule = get_vehicule_by_id(pk)
        if not vehicule:
            return Response({'error': 'Introuvable'}, status=404)
        desactiver_vehicule(vehicule)
        return Response(status=204)