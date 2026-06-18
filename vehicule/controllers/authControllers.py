from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from vehicule.dto import (
    LoginDemandeurSerializer,
    DemandeurSerializer,
    LoginAdminSerializer,
    LoginadminSerializer,
    CreerLoginadminSerializer,
)
from vehicule.services import (
    connecter_utilisateur,
    connecter_admin,
    get_tokens_for_user,
    get_admin_session,
    register_admin
)
class LoginController(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        ser = LoginDemandeurSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)

        user, error = connecter_utilisateur(
            ser.validated_data['email'],
            ser.validated_data['password'],
            request,
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
    authentication_classes = [] 

    def post(self, request):
        ser = LoginAdminSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)

        admin = connecter_admin(
            ser.validated_data['email'],
            ser.validated_data['password'],
        )
        if not admin:
            return Response({'error': 'Identifiants invalides'}, status=401)

        admin.derniere_connexion = timezone.now()
        admin.save(update_fields=['derniere_connexion'])

        refresh = RefreshToken()
        
        refresh['user_id'] = admin.pk
        refresh['type'] = 'admin'
        refresh['username'] = admin.username

        return Response({
            'type': 'admin',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
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

class RegisterAdminController(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [] 
    def post(self, request):
        serializer = CreerLoginadminSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        validated_data = serializer.validated_data
        try:
            new_admin = register_admin(
                username=validated_data['username'],
                password=validated_data['password'],
                email=validated_data['email'],
                nom=validated_data['nom'],
                prenom=validated_data['prenom']
            )
            
            return Response({
                "message": "Administrateur créé avec succès !",
                "admin": {
                    "id": new_admin.id,
                    "username": new_admin.username,
                    "email": new_admin.email
                }
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)