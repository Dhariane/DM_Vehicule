from rest_framework import serializers
from vehicule.models import Demandeur


class DemandeurSerializer(serializers.ModelSerializer):
    chef_direct_nom = serializers.SerializerMethodField()

    class Meta:
        model = Demandeur
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'telephone',
            'service',
            'poste',
            'chef_direct',
            'chef_direct_nom',
            'is_active',
        ]

    def get_chef_direct_nom(self, obj):
        if obj.chef_direct:
            return obj.chef_direct.get_full_name() or obj.chef_direct.username
        return None


class CreerDemandeurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Demandeur
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'role',
            'telephone',
            'service',
            'poste',
            'chef_direct',
        ]

    def validate_chef_direct(self, value):
        if value and value.role != 'Chef':
            raise serializers.ValidationError(
                "Le chef direct doit avoir le rôle Chef."
            )
        return value

    def validate_username(self, value):
        if Demandeur.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Ce nom d'utilisateur est déjà pris."
            )
        return value

    def validate_email(self, value):
        if Demandeur.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Cet email est déjà utilisé."
            )
        return value

    def create(self, validated_data):
        from vehicule.services import creer_demandeur
        return creer_demandeur(validated_data)


class UpdateDemandeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demandeur
        fields = [
            'first_name',
            'last_name',
            'email',
            'role',
            'telephone',
            'service',
            'poste',
            'chef_direct',
            'is_active',
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
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

class ChefOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demandeur
        fields = ['id', 'username', 'first_name', 'last_name']