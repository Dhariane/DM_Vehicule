from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from permission import IsJWTAdmin
from vehicule.controllers.adminControllers import check_admin
from vehicule.dto import (
    DemandeurSerializer,
    CreerDemandeurSerializer,
    UpdateDemandeurSerializer,
)
from vehicule.models.demandeur import Demandeur
from vehicule.services import (
    get_all_demandeurs,
    get_demandeur_by_id,
    creer_demandeur,
    modifier_demandeur,
    desactiver_demandeur,
)


class DemandeurListCreateController(APIView):
    permission_classes = [IsJWTAdmin]

    def get(self, request):
        err = check_admin(request)
        if err:
            return err
        users = get_all_demandeurs()
        # ✅ Retourner au format paginé attendu par le frontend
        serialized = DemandeurSerializer(users, many=True).data
        return Response({
            'results': serialized,
            'count': len(serialized),
        })

    def post(self, request):
        ser = CreerDemandeurSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        user = creer_demandeur(ser.validated_data)
        return Response(DemandeurSerializer(user).data, status=201)


class DemandeurDetailController(APIView):
    permission_classes = [IsJWTAdmin]

    def get(self, request, pk):
        user = get_demandeur_by_id(pk)
        if not user:
            return Response({'error': 'Introuvable'}, status=404)
        return Response(DemandeurSerializer(user).data)

    def put(self, request, pk):
        user = get_demandeur_by_id(pk)
        if not user:
            return Response({'error': 'Introuvable'}, status=404)
        ser = UpdateDemandeurSerializer(user, data=request.data, partial=True)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        user = modifier_demandeur(user, ser.validated_data)
        return Response(DemandeurSerializer(user).data)

    def delete(self, request, pk):
        user = get_demandeur_by_id(pk)
        if not user:
            return Response({'error': 'Introuvable'}, status=404)
        desactiver_demandeur(user)
        return Response(status=204)