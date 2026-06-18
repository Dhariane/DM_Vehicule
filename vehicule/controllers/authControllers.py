from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from vehicule.dto import (
    LoginDemandeurSerializer,
    DemandeurSerializer,
    LoginAdminSerializer,
    LoginadminSerializer,
)
from vehicule.services import connecter_admin, get_admin_session


class LoginController(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = LoginDemandeurSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)

        user = authenticate(
            request,
            username=ser.validated_data['username'],
            password=ser.validated_data['password'],
        )
        if not user:
            return Response({'error': 'Identifiants invalides'}, status=401)
        if not user.is_active:
            return Response({'error': 'Compte désactivé'}, status=403)

        login(request, user)
        return Response({
            'type': 'utilisateur',
            **DemandeurSerializer(user).data,
        })


class LogoutController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Déconnexion réussie'})


class MeController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'type': 'utilisateur',
            **DemandeurSerializer(request.user).data,
        })


class LoginAdminController(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = LoginAdminSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)

        admin = connecter_admin(
            ser.validated_data['username'],
            ser.validated_data['password'],
        )
        if not admin:
            return Response({'error': 'Identifiants invalides'}, status=401)

        request.session['admin_id'] = admin.pk
        request.session['admin_username'] = admin.username

        return Response({
            'type': 'admin',
            **LoginadminSerializer(admin).data,
        })


class LogoutAdminController(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        request.session.flush()
        return Response({'message': 'Déconnexion admin réussie'})


class MeAdminController(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        admin = get_admin_session(request)
        if not admin:
            return Response({'error': 'Non connecté'}, status=401)
        return Response({
            'type': 'admin',
            **LoginadminSerializer(admin).data,
        })