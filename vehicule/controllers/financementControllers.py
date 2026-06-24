from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from vehicule.dto.financementDto import FinancementSerializer, CreerFinancementSerializer
from vehicule.services.financementService import (
    get_all_financements,
    get_financement_by_id,
    creer_financement,
    modifier_financement,
    supprimer_financement,
)


class FinancementListCreateController(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        financements = get_all_financements()
        return Response(FinancementSerializer(financements, many=True).data)

    def post(self, request):
        if not is_admin(request):
            return Response({'error': 'Accès réservé à l\'admin'}, status=403)
        ser = CreerFinancementSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        financement = creer_financement(ser.validated_data)
        return Response(FinancementSerializer(financement).data, status=201)


class FinancementDetailController(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        financement = get_financement_by_id(pk)
        if not financement:
            return Response({'error': 'Introuvable'}, status=404)
        return Response(FinancementSerializer(financement).data)

    def put(self, request, pk):
        if not is_admin(request):
            return Response({'error': 'Accès réservé'}, status=403)
        financement = get_financement_by_id(pk)
        if not financement:
            return Response({'error': 'Introuvable'}, status=404)
        ser = CreerFinancementSerializer(financement, data=request.data, partial=True)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        financement = modifier_financement(financement, ser.validated_data)
        return Response(FinancementSerializer(financement).data)

    def delete(self, request, pk):
        if not is_admin(request):
            return Response({'error': 'Accès réservé'}, status=403)
        financement = get_financement_by_id(pk)
        if not financement:
            return Response({'error': 'Introuvable'}, status=404)
        supprimer_financement(financement)
        return Response(status=204)