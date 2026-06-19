from rest_framework import serializers
from vehicule.models import Chauffeur
from vehicule.models.financement import Financement
from vehicule.dto.financementDto import FinancementSerializer  # Pour l'affichage imbriqué


class ChauffeurSerializer(serializers.ModelSerializer):
    # Permet d'avoir l'objet Financement complet dans le JSON de réponse
    financement = FinancementSerializer(read_only=True)

    class Meta:
        model = Chauffeur
        fields = [
            'id',
            'nom',
            'prenom',
            'telephone',
            'email',
            'disponible',
            'financement',  
            'date_creation',
        ]


class CreerChauffeurSerializer(serializers.ModelSerializer):
    # On attend l'ID du financement venant de Next.js
    financement_id = serializers.PrimaryKeyRelatedField(
        queryset=Financement.objects.all(),
        source='financement',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Chauffeur
        fields = [
            'nom',
            'prenom',
            'telephone',
            'email',
            'financement_id',
        ]

    def validate_telephone(self, value):
        if Chauffeur.objects.filter(telephone=value).exists():
            raise serializers.ValidationError("Ce numéro de téléphone est déjà utilisé.")
        return value

    def create(self, validated_data):
        from vehicule.services import creer_chauffeur
        return creer_chauffeur(**validated_data)


class UpdateChauffeurSerializer(serializers.ModelSerializer):
    financement_id = serializers.PrimaryKeyRelatedField(
        queryset=Financement.objects.all(),
        source='financement',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Chauffeur
        fields = [
            'nom',
            'prenom',
            'telephone',
            'email',
            'disponible',
            'financement_id',
        ]

    def update(self, instance, validated_data):
        from vehicule.services import modifier_chauffeur
        return modifier_chauffeur(instance, validated_data)