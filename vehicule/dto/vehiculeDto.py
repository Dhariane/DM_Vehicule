from rest_framework import serializers
from vehicule.models import Vehicule


class VehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = [
            'id',
            'immatriculation',
            'marque',
            'modele',
            'disponible',
        ]


class CreerVehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = [
            'immatriculation',
            'marque',
            'modele',
        ]

    def validate_immatriculation(self, value):
        if Vehicule.objects.filter(immatriculation=value).exists():
            raise serializers.ValidationError(
                "Cette immatriculation existe déjà."
            )
        return value

    def create(self, validated_data):
        from vehicule.services import creer_vehicule
        return creer_vehicule(validated_data)


class UpdateVehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = [
            'immatriculation',
            'marque',
            'modele',
            'disponible',
        ]

    def update(self, instance, validated_data):
        from vehicule.services import modifier_vehicule
        return modifier_vehicule(instance, validated_data)