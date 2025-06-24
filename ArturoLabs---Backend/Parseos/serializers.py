from rest_framework import serializers
from .models import Nino, Embarazo, ControlDeSalud, Vacunas

class NinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nino
        fields = '__all__'

class EmbarazoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Embarazo
        fields = '__all__'

class ControlDeSaludSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlDeSalud
        fields = '__all__'

class VacunasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacunas
        fields = '__all__'
