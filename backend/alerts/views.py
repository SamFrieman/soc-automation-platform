from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from alerts.models import Alert, AlertComment
from alerts.serializers import AlertSerializer, AlertCommentSerializer
from alerts.tasks import process_alert


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['severity', 'status', 'source_system']
    search_fields = ['title', 'description', 'alert_id']
    ordering_fields = ['detected_at', 'severity']
    ordering = ['-detected_at']
    
    def perform_create(self, serializer):
        alert = serializer.save()
        # Trigger background processing
        process_alert.delay(alert.id)
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        alert.status = 'RESOLVED'
        alert.save()
        return Response({'status': 'alert resolved'})
    
    @action(detail=True, methods=['post'])
    def classify(self, request, pk=None):
        alert = self.get_object()
        process_alert.delay(alert.id)
        return Response({'status': 'classification started'})


class AlertCommentViewSet(viewsets.ModelViewSet):
    queryset = AlertComment.objects.all()
    serializer_class = AlertCommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)