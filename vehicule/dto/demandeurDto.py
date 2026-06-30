import secrets
import string
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from vehicule.models import Demandeur


class DemandeurSerializer(serializers.ModelSerializer):
    chef_direct_nom = serializers.SerializerMethodField()

    class Meta:
        model = Demandeur
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'role', 'telephone', 'service', 'poste',
            'chef_direct', 'chef_direct_nom', 'is_active',
        ]

    def get_chef_direct_nom(self, obj):
        if obj.chef_direct:
            return obj.chef_direct.get_full_name() or obj.chef_direct.username
        return None


class CreerDemandeurSerializer(serializers.ModelSerializer):
    """✅ Pas de champ password — généré automatiquement et envoyé par email."""

    class Meta:
        model = Demandeur
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'role', 'telephone', 'service', 'poste', 'chef_direct',
        ]

    def validate_chef_direct(self, value):
        if value and value.role != 'Chef':
            raise serializers.ValidationError(
                "Le chef direct doit avoir le rôle Chef."
            )
        return value

    def validate_username(self, value):
        if Demandeur.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return value

    def validate_email(self, value):
        if Demandeur.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def create(self, validated_data):
        # ✅ Générer un mot de passe aléatoire sécurisé
        alphabet = string.ascii_letters + string.digits + '!@#$%'
        password = ''.join(secrets.choice(alphabet) for _ in range(10))

        user = Demandeur(**validated_data)
        user.set_password(password)
        user.save()

        # ✅ Version texte brut (de secours si l'application de messagerie de l'utilisateur bloque le HTML)
        texte_secours = f"""Bonjour {user.first_name} {user.last_name},

Votre compte a été configuré avec succès sur l'application UCP Santé.

Identifiants d'accès :
- Email : {user.email}
- Mot de passe : {password}

Lien de connexion : https://localhost:3000

Cordialement,
L'équipe UCP Santé"""

        # ✅ Version HTML visuelle complète
        code_html = f"""<!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; background-color: #f3f4f6; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #374151;">
            <table width="100%" border="0" cellpadding="0" cellspacing="0" style="background-color: #f3f4f6; padding: 30px 15px;">
                <tr>
                    <td align="center">
                        <table width="100%" max-width="500" border="0" cellpadding="0" cellspacing="0" style="max-width: 500px; background-color: #ffffff; border-radius: 20px; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden;">
                            <tr>
                                <td style="background-color: #00b074; padding: 24px 30px;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 20px; font-weight: 800;">UCP Santé</h1>
                                    <p style="margin: 2px 0 0 0; color: #e6f7f1; font-size: 12px; font-weight: 500;">Gestion de la Flotte Automobile</p>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 30px;">
                                    <p style="margin: 0 0 16px 0; font-size: 15px; font-weight: 700; color: #111827;">Bonjour {user.first_name} {user.last_name},</p>
                                    <p style="margin: 0 0 20px 0; font-size: 13px; line-height: 20px; color: #4b5563;">Votre compte a été configuré avec succès. Voici vos identifiants d'accès sécurisés :</p>
                                    
                                    <table width="100%" border="0" cellpadding="0" cellspacing="0" style="background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 12px; margin-bottom: 24px;">
                                        <tr>
                                            <td style="padding: 16px 20px;">
                                                <table width="100%" border="0" cellpadding="0" cellspacing="0">
                                                    <tr>
                                                        <td width="30%" style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #9ca3af; padding-bottom: 8px;">Email :</td>
                                                        <td style="font-size: 13px; font-weight: 600; color: #111827; padding-bottom: 8px; font-family: monospace;">{user.email}</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #9ca3af; padding-top: 8px; border-top: 1px solid #f3f4f6;">Mot de passe :</td>
                                                        <td style="font-size: 13px; font-weight: 600; color: #00b074; padding-top: 8px; border-top: 1px solid #f3f4f6; font-family: monospace;">{password}</td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>

                                    <table width="100%" border="0" cellpadding="0" cellspacing="0" style="margin-bottom: 24px;">
                                        <tr>
                                            <td align="center">
                                                <a href="https://votre-application.ucpsante.org/login" target="_blank" style="display: inline-block; background-color: #00b074; color: #ffffff; font-size: 12px; font-weight: 700; text-decoration: none; padding: 12px 28px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 176, 116, 0.15);">
                                                    Se connecter à l'application
                                                </a>
                                            </td>
                                        </tr>
                                    </table>

                                    <p style="margin: 0; font-size: 10px; line-height: 14px; color: #9ca3af; border-top: 1px solid #f3f4f6; padding-top: 16px;">
                                        🔒 <strong>Sécurité :</strong> Modifiez ce mot de passe temporaire dès votre première connexion depuis les paramètres de votre compte.
                                    </p>
                                </td>
                            </tr>
                            <tr>
                                <td style="background-color: #fafafa; border-top: 1px solid #e5e7eb; padding: 16px 30px; text-align: center;">
                                    <p style="margin: 0; font-size: 11px; color: #6b7280;">Cordialement,<br><span style="font-weight: 700; color: #111827;">L'équipe UCP Santé</span></p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>"""

        # ✅ Envoyer les identifiants par email avec gestion du HTML
        try:
            send_mail(
                subject='🔐 Vos identifiants UCP Santé — Gestion des Véhicules',
                message=texte_secours,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
                html_message=code_html,
            )
            print(f"[EMAIL] Identifiants envoyés à {user.email}")
        except Exception as e:
            print(f"[EMAIL] Erreur envoi identifiants à {user.email}: {e}")

        return user


class UpdateDemandeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demandeur
        fields = [
            'first_name', 'last_name', 'email', 'role',
            'telephone', 'service', 'poste', 'chef_direct', 'is_active',
        ]

    def validate_chef_direct(self, value):
        if value and value.role != 'Chef':
            raise serializers.ValidationError(
                "Le chef direct doit avoir le rôle Chef."
            )
        return value

    def update(self, instance, validated_data):
        from vehicule.services import modifier_demandeur
        return modifier_demandeur(instance, validated_data)


class LoginDemandeurSerializer(serializers.Serializer):
    email    = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)


class ChefOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Demandeur
        fields = ['id', 'username', 'first_name', 'last_name']