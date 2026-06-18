from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from vehicule.dto import (
    LoginDemandeurSerializer,
    DemandeurSerializer,
    LoginAdminSerializer,
    LoginadminSerializer,
)
from vehicule.services import (
    connecter_utilisateur,
    connecter_admin,
    get_tokens_for_user,
    get_admin_session,
)


class LoginController(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = LoginDemandeurSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)

        user, error = connecter_utilisateur(
            ser.validated_data['email'],       # ← email
            ser.validated_data['password'],
        )
        if error:
            return Response({'error': error}, status=401)

        tokens = get_tokens_for_user(user)
        return Response({
            'type': 'utilisateur',
            'access': tokens['access'],
            'refresh': tokens['refresh'],
            **DemandeurSerializer(user).data,
        })


class LogoutController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
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
            ser.validated_data['email'],       # ← email
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