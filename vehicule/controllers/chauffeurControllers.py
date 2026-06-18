from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from permission import IsJWTAdmin
from vehicule.dto import ChauffeurSerializer, CreerChauffeurSerializer
from vehicule.services import (
    get_all_chauffeurs,
    get_chauffeur_by_id,
    creer_chauffeur,
    modifier_chauffeur,
    desactiver_chauffeur,
)


class ChauffeurListCreateController(APIView):
    permission_classes = [IsJWTAdmin]

    def get(self, request):
        chauffeurs = get_all_chauffeurs()
        return Response(ChauffeurSerializer(chauffeurs, many=True).data)

    def post(self, request):
        ser = CreerChauffeurSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        chauffeur = creer_chauffeur(ser.validated_data)
        return Response(ChauffeurSerializer(chauffeur).data, status=201)


class ChauffeurDetailController(APIView):
    permission_classes = [IsJWTAdmin]

    def get(self, request, pk):
        chauffeur = get_chauffeur_by_id(pk)
        if not chauffeur:
            return Response({'error': 'Introuvable'}, status=404)
        return Response(ChauffeurSerializer(chauffeur).data)

    def put(self, request, pk):
        chauffeur = get_chauffeur_by_id(pk)
        if not chauffeur:
            return Response({'error': 'Introuvable'}, status=404)
        ser = ChauffeurSerializer(chauffeur, data=request.data, partial=True)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        chauffeur = modifier_chauffeur(chauffeur, ser.validated_data)
        return Response(ChauffeurSerializer(chauffeur).data)

    def delete(self, request, pk):
        chauffeur = get_chauffeur_by_id(pk)
        if not chauffeur:
            return Response({'error': 'Introuvable'}, status=404)
        desactiver_chauffeur(chauffeur)
        return Response(status=204)