from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from vehicule.models import Loginadmin


class LoginadminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loginadmin
        fields = [
            'id',
            'username',
            'email',
            'nom',
            'prenom',
            'is_active',
            'derniere_connexion',
        ]


class CreerLoginadminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Loginadmin
        fields = [
            'username',
            'email',
            'nom',
            'prenom',
            'password',
        ]

    def validate_username(self, value):
        if Loginadmin.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Ce nom d'utilisateur admin est déjà pris."
            )
        return value

    def validate_email(self, value):
        if Loginadmin.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Cet email admin est déjà utilisé."
            )
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return Loginadmin.objects.create(**validated_data)


class LoginAdminSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)