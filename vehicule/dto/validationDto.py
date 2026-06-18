from rest_framework import serializers
from vehicule.models import ValidationDemande


class ValidationDemandeSerializer(serializers.ModelSerializer):
    validateur_nom = serializers.SerializerMethodField()
    etape_display = serializers.CharField(
        source='get_etape_display', read_only=True
    )
    decision_display = serializers.CharField(
        source='get_decision_display', read_only=True
    )

    class Meta:
        model = ValidationDemande
        fields = [
            'id',
            'demande',
            'validateur',
            'validateur_nom',
            'etape',
            'etape_display',
            'decision',
            'decision_display',
            'commentaire',
            'date_validation',
        ]

    def get_validateur_nom(self, obj):
        return obj.validateur.get_full_name() or obj.validateur.username


class ValiderDemandeSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=['approuve', 'rejete'])
    commentaire = serializers.CharField(
        required=False, allow_blank=True, default=''
    )
    vehicule_id = serializers.IntegerField(required=False, allow_null=True)
    chauffeur_id = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, data):
        # Si logistique approuve, vehicule_id est obligatoire
        if data.get('decision') == 'approuve':
            if not data.get('vehicule_id') and not data.get('chauffeur_id'):
                # On laisse passer — la vérif se fait dans le service
                # selon l'étape courante
                pass
        return data