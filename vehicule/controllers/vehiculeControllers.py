from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from vehicule.dto import VehiculeSerializer, CreerVehiculeSerializer
from vehicule.services import (
    is_admin,
    get_all_vehicules,
    get_vehicule_by_id,
    creer_vehicule,
    modifier_vehicule,
    desactiver_vehicule,
)


class VehiculeListCreateController(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        vehicules = get_all_vehicules()
        return Response(VehiculeSerializer(vehicules, many=True).data)

    def post(self, request):
        if not is_admin(request):
            return Response({'error': 'Accès réservé à l\'admin'}, status=403)
        ser = CreerVehiculeSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        vehicule = creer_vehicule(ser.validated_data)
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