from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from permission import IsJWTAdminOrLogistique
from vehicule.dto import VehiculeSerializer
from vehicule.dto.demandeVehiculeDto import DemandeVehiculeSerializer
from vehicule.services.authService import is_admin
from vehicule.services.vehiculeService import (
    get_all_vehicules,
    get_vehicules_disponibles,
    get_vehicules_disponibles_pour,
    get_vehicules_en_mission,
    get_vehicule_by_id,
    creer_vehicule,
    modifier_vehicule,
    desactiver_vehicule,
    
)


class VehiculeListCreateController(APIView):
    permission_classes = [IsJWTAdminOrLogistique]

    def get(self, request):
        # Logistique voit tous les véhicules
        vehicules = get_all_vehicules()
        return Response(VehiculeSerializer(vehicules, many=True).data)

    def post(self, request):
        if not is_admin(request):
            return Response({'error': 'Accès réservé à l\'admin'}, status=403)
        ser = VehiculeSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        vehicule = creer_vehicule(ser.validated_data)
        return Response(VehiculeSerializer(vehicule).data, status=201)


class VehiculeDisponibleController(APIView):
    """Véhicules disponibles pour une période donnée."""
    permission_classes = [IsJWTAdminOrLogistique]

    def get(self, request):
        date_depart = request.query_params.get('date_depart')
        date_retour = request.query_params.get('date_retour')

        if date_depart and date_retour:
            from django.utils.dateparse import parse_datetime
            vehicules = get_vehicules_disponibles_pour(
                parse_datetime(date_depart),
                parse_datetime(date_retour),
            )
        else:
            vehicules = get_vehicules_disponibles()

        return Response(VehiculeSerializer(vehicules, many=True).data)


class MissionsEnCoursController(APIView):
    """Liste des missions en cours — pour le logistique."""
    permission_classes = [IsJWTAdminOrLogistique]

    def get(self, request):
        demandes = get_vehicules_en_mission()
        data = []
        for d in demandes:
            data.append({
                'id': d.id,
                'destination': d.destination,
                'demandeur_nom': d.demandeur.get_full_name() or d.demandeur.username,
                'date_depart': d.date_depart,
                'date_retour': d.date_retour,
                'vehicule': f"{d.vehicule.marque} {d.vehicule.modele} ({d.vehicule.immatriculation})" if d.vehicule else '-',
                'chauffeur': f"{d.chauffeur.prenom} {d.chauffeur.nom}" if d.chauffeur else '-',
            })
        return Response(data)
    

# Ajoute à la fin de vehiculeControllers.py

class VehiculeDetailController(APIView):
    permission_classes = [IsJWTAdminOrLogistique]

    def get(self, request, pk):
        vehicule = get_vehicule_by_id(pk)
        if not vehicule:
            return Response({'error': 'Introuvable'}, status=404)
        return Response(VehiculeSerializer(vehicule).data)

    def put(self, request, pk):
        vehicule = get_vehicule_by_id(pk)
        if not vehicule:
            return Response({'error': 'Introuvable'}, status=404)
        ser = VehiculeSerializer(vehicule, data=request.data, partial=True)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        vehicule = modifier_vehicule(vehicule, ser.validated_data)
        return Response(VehiculeSerializer(vehicule).data)

    def delete(self, request, pk):
        vehicule = get_vehicule_by_id(pk)
        if not vehicule:
            return Response({'error': 'Introuvable'}, status=404)
        desactiver_vehicule(vehicule)
        return Response(status=204)