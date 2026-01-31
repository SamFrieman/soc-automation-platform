from rest_framework import serializers
from alerts.models import Alert, AlertComment
from frameworks.models import MitreTechnique, OwaspCategory


class AlertSerializer(serializers.ModelSerializer):
    mitre_techniques = serializers.StringRelatedField(many=True, read_only=True)
    owasp_categories = serializers.StringRelatedField(many=True, read_only=True)
    stride_categories = serializers.StringRelatedField(many=True, read_only=True)
    kill_chain_stage = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AlertCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = AlertComment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'user']