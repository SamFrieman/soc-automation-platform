from rest_framework import serializers
from playbooks.models import Playbook, PlaybookExecution


class PlaybookSerializer(serializers.ModelSerializer):
    mitre_techniques = serializers.StringRelatedField(many=True, read_only=True)
    owasp_categories = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Playbook
        fields = '__all__'
        read_only_fields = ['execution_count', 'success_count', 'failure_count', 'created_at', 'updated_at']


class PlaybookExecutionSerializer(serializers.ModelSerializer):
    playbook = serializers.StringRelatedField(read_only=True)
    alert = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = PlaybookExecution
        fields = '__all__'
        read_only_fields = ['started_at', 'completed_at', 'created_at']