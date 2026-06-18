from rest_framework import serializers
from django.utils import timezone
from vehicule.models import DemandeVehicule
from vehicule.dto.vehiculeDto import VehiculeSerializer
from vehicule.dto.chauffeurDto import ChauffeurSerializer
from vehicule.dto.validationDto import ValidationDemandeSerializer


class DemandeVehiculeSerializer(serializers.ModelSerializer):
    demandeur_nom = serializers.SerializerMethodField()
    demandeur_poste = serializers.SerializerMethodField()
    demandeur_email = serializers.SerializerMethodField()
    chef_direct_nom = serializers.SerializerMethodField()
    vehicule_info = VehiculeSerializer(source='vehicule', read_only=True)
    chauffeur_info = ChauffeurSerializer(source='chauffeur', read_only=True)
    validations = ValidationDemandeSerializer(many=True, read_only=True)
    statut_display = serializers.CharField(
        source='get_statut_display', read_only=True
    )
    etape_display = serializers.CharField(
        source='get_etape_validation_display', read_only=True
    )

    class Meta:
        model = DemandeVehicule
        fields = [
            'id',
            'demandeur',
            'demandeur_nom',
            'demandeur_poste',
            'demandeur_email',
            'chef_direct_nom',
            'vehicule',
            'vehicule_info',
            'chauffeur',
            'chauffeur_info',
            'motif',
            'destination',
            'description',
            'date_depart',
            'date_retour',
            'nombre_passagers',
            'statut',
            'statut_display',
            'etape_validation',
            'etape_display',
            'validations',
            'date_creation',
            'date_modification',
        ]

    def get_demandeur_nom(self, obj):
        return obj.demandeur.get_full_name() or obj.demandeur.username

    def get_demandeur_poste(self, obj):
        return obj.demandeur.poste

    def get_demandeur_email(self, obj):
        return obj.demandeur.email

    def get_chef_direct_nom(self, obj):
        chef = obj.demandeur.chef_direct
        if chef:
            return chef.get_full_name() or chef.username
        return None


class CreerDemandeSerializer(serializers.Serializer):
    motif = serializers.ChoiceField(choices=DemandeVehicule.MOTIF_CHOICES)
    destination = serializers.CharField(max_length=200)
    description = serializers.CharField(
        required=False, allow_blank=True, default=''
    )
    date_depart = serializers.DateTimeField()
    date_retour = serializers.DateTimeField()
    nombre_passagers = serializers.IntegerField(min_value=1, default=1)

    def validate_date_depart(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "La date de départ doit être dans le futur."
            )
        return value

    def validate(self, data):
        if data.get('date_retour') and data.get('date_depart'):
            if data['date_retour'] <= data['date_depart']:
                raise serializers.ValidationError(
                    "La date de retour doit être après la date de départ."
                )
        return data