from rest_framework import serializers
from .models import *

class NiñoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niño
        fields = '__all__'


class TutorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'




class AutenticacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autenticacion
        fields = '__all__'
