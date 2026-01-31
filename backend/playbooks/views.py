from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from playbooks.models import Playbook, PlaybookExecution
from playbooks.serializers import PlaybookSerializer, PlaybookExecutionSerializer
from playbooks.tasks import execute_playbook_script


class PlaybookViewSet(viewsets.ModelViewSet):
    queryset = Playbook.objects.all()
    serializer_class = PlaybookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['playbook_type', 'enabled', 'auto_execute']
    search_fields = ['name', 'description']
    
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        playbook = self.get_object()
        alert_id = request.data.get('alert_id')
        
        if not alert_id:
            return Response({'error': 'alert_id required'}, status=400)
        
        from alerts.models import Alert
        try:
            alert = Alert.objects.get(id=alert_id)
        except Alert.DoesNotExist:
            return Response({'error': 'Alert not found'}, status=404)
        
        execution = PlaybookExecution.objects.create(
            playbook=playbook,
            alert=alert,
            triggered_by=request.user,
            status='PENDING'
        )
        
        execute_playbook_script.delay(execution.id)
        
        return Response({
            'execution_id': execution.id,
            'status': 'Playbook execution started'
        })


class PlaybookExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlaybookExecution.objects.all()
    serializer_class = PlaybookExecutionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'playbook']