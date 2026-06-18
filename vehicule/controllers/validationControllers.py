from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from vehicule.models import DemandeVehicule
from vehicule.dto import DemandeVehiculeSerializer, ValiderDemandeSerializer
from vehicule.services import demandes_a_valider, traiter_validation


class ValidationListController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        demandes = demandes_a_valider(request.user)
        return Response(DemandeVehiculeSerializer(demandes, many=True).data)


class ValidationActionController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            demande = DemandeVehicule.objects.select_related(
                'demandeur', 'vehicule', 'chauffeur'
            ).get(pk=pk)
        except DemandeVehicule.DoesNotExist:
            return Response({'error': 'Demande introuvable'}, status=404)

        ser = ValiderDemandeSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)

        try:
            demande = traiter_validation(
                demande=demande,
                validateur=request.user,
                decision=ser.validated_data['decision'],
                commentaire=ser.validated_data.get('commentaire', ''),
                vehicule_id=ser.validated_data.get('vehicule_id'),
                chauffeur_id=ser.validated_data.get('chauffeur_id'),
            )
            return Response(DemandeVehiculeSerializer(demande).data)
        except ValueError as e:
            return Response({'error': str(e)}, status=400)