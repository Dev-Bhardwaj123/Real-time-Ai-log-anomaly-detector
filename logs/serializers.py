from rest_framework import serializers
from .models import AnomalyLog

class AnomalyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnomalyLog
        fields = '__all__'
