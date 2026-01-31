from rest_framework import viewsets, views
from rest_framework.response import Response
from django.db.models import Count, Avg
from analytics.models import DailyMetrics
from analytics.serializers import DailyMetricsSerializer
from alerts.models import Alert
from incidents.models import Incident
from playbooks.models import PlaybookExecution


class DailyMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyMetrics.objects.all()
    serializer_class = DailyMetricsSerializer
    ordering = ['-date']


class DashboardStatsView(views.APIView):
    """Real-time dashboard statistics"""
    
    def get(self, request):
        # Alert statistics
        total_alerts = Alert.objects.count()
        new_alerts = Alert.objects.filter(status='NEW').count()
        critical_alerts = Alert.objects.filter(severity='CRITICAL').count()
        
        alerts_by_severity = Alert.objects.values('severity').annotate(
            count=Count('id')
        )
        
        # Incident statistics
        total_incidents = Incident.objects.count()
        open_incidents = Incident.objects.filter(status='OPEN').count()
        
        # Playbook statistics
        total_executions = PlaybookExecution.objects.count()
        successful_executions = PlaybookExecution.objects.filter(status='SUCCESS').count()
        
        # Top MITRE techniques
        from frameworks.models import MitreTechnique
        top_techniques = []
        for technique in MitreTechnique.objects.annotate(
            alert_count=Count('alerts')
        ).order_by('-alert_count')[:5]:
            top_techniques.append({
                'technique_id': technique.technique_id,
                'name': technique.name,
                'count': technique.alert_count
            })
        
        return Response({
            'alerts': {
                'total': total_alerts,
                'new': new_alerts,
                'critical': critical_alerts,
                'by_severity': list(alerts_by_severity),
            },
            'incidents': {
                'total': total_incidents,
                'open': open_incidents,
            },
            'playbooks': {
                'total_executions': total_executions,
                'successful': successful_executions,
                'success_rate': (successful_executions / total_executions * 100) if total_executions > 0 else 0,
            },
            'top_mitre_techniques': top_techniques,
        })