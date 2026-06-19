from rest_framework import serializers
from vehicule.models.financement import Financement


class FinancementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financement
        fields = [
            'id',
            'nom',
        ]


class CreerFinancementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financement
        fields = [
            'nom',
        ]

    def validate_nom(self, value):
        if Financement.objects.filter(nom=value).exists():
            raise serializers.ValidationError(
                "Un financement avec ce nom existe déjà."
            )
        return value