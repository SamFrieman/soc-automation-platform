from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from incidents.models import Incident
from incidents.serializers import IncidentSerializer


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['severity', 'status', 'incident_type']
    search_fields = ['title', 'description', 'incident_id']
    ordering = ['-detected_at']