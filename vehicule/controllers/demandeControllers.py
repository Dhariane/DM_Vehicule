from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from vehicule.dto import DemandeVehiculeSerializer, CreerDemandeSerializer
from vehicule.services import (
    get_mes_demandes,
    get_demande_by_id,
    creer_demande,
    annuler_demande,
)


class MesDemandesController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        demandes = get_mes_demandes(request.user)
        return Response(DemandeVehiculeSerializer(demandes, many=True).data)

    def post(self, request):
        ser = CreerDemandeSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        try:
            demande = creer_demande(request.user, ser.validated_data)
            return Response(DemandeVehiculeSerializer(demande).data, status=201)
        except ValueError as e:
            return Response({'error': str(e)}, status=400)


class DetailDemandeController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        demande = get_demande_by_id(pk, request.user)
        if not demande:
            return Response({'error': 'Introuvable'}, status=404)
        return Response(DemandeVehiculeSerializer(demande).data)

    def delete(self, request, pk):
        demande = get_demande_by_id(pk, request.user)
        if not demande:
            return Response({'error': 'Introuvable'}, status=404)
        try:
            annuler_demande(demande)
            return Response(status=204)
        except ValueError as e:
            return Response({'error': str(e)}, status=400)