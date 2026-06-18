from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from vehicule.models import Loginadmin  # Ajuste l'import selon ta structure

class HybridJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        raw_token = auth_header.split(' ')[1]
        jwt_auth = JWTAuthentication()

        try:
            # On valide le token JWT
            validated_token = jwt_auth.get_validated_token(raw_token)
            
            # CAS 1 : C'est un Administrateur (Custom token)
            if validated_token.get('type') == 'admin':
                admin_id = validated_token.get('user_id')
                try:
                    admin = Loginadmin.objects.get(pk=admin_id, is_active=True)
                    # On attache temporairement un attribut à la request pour nos permissions
                    request.meta_is_admin = True
                    # On retourne un utilisateur anonyme (ou l'admin) pour DRF, mais SANS planter
                    return (AnonymousUser(), validated_token)
                except Loginadmin.DoesNotExist:
                    raise AuthenticationFailed("Administrateur introuvable")

            # CAS 2 : C'est un Demandeur standard (Authentification DRF classique)
            user = jwt_auth.get_user(validated_token)
            request.meta_is_admin = False
            return (user, validated_token)

        except Exception as e:
            raise AuthenticationFailed(str(e))