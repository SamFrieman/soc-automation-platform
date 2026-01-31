from rest_framework import serializers
from incidents.models import Incident


class IncidentSerializer(serializers.ModelSerializer):
    alerts = serializers.StringRelatedField(many=True, read_only=True)
    assigned_to = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Incident
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']