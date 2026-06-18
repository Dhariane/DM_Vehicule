from rest_framework import serializers
from vehicule.models import Chauffeur


class ChauffeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chauffeur
        fields = [
            'id',
            'nom',
            'prenom',
            'telephone',
            'email',
            'disponible',
            'date_creation',
        ]


class CreerChauffeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chauffeur
        fields = [
            'nom',
            'prenom',
            'telephone',
            'email',
        ]

    def validate_telephone(self, value):
        if Chauffeur.objects.filter(telephone=value).exists():
            raise serializers.ValidationError(
                "Ce numéro de téléphone est déjà utilisé."
            )
        return value

    def create(self, validated_data):
        from vehicule.services import creer_chauffeur
        return creer_chauffeur(validated_data)


class UpdateChauffeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chauffeur
        fields = [
            'nom',
            'prenom',
            'telephone',
            'email',
        ]

    def update(self, instance, validated_data):
        from vehicule.services import modifier_chauffeur
        return modifier_chauffeur(instance, validated_data)