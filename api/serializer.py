from rest_framework import serializers
from .models import DataTimeMicro

class DataTimeMicroSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataTimeMicro
        fields = '__all__'