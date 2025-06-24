from rest_framework import serializers
from .models import *

class NinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nino
        fields = '__all__'


class TutorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key.lower(): value for key, value in data.items()}



class AutenticacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autenticacion
        fields = '__all__'


class ControlSerializer(serializers.ModelSerializer):
    IMC = serializers.SerializerMethodField()

    class Meta:
        model = Control
        fields = '__all__' # Include all fields from the model

    def get_IMC(self, obj):
        try:
            peso = float(obj.peso)
            talla_m = float(obj.talla) / 100
            if talla_m == 0:
                return None
            imc_value = peso / (talla_m * talla_m)
            return round(imc_value, 2)
        except (ValueError, TypeError):
            return None

    

