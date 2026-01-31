from celery import shared_task
from analytics.models import DailyMetrics
from alerts.models import Alert
from incidents.models import Incident
from playbooks.models import PlaybookExecution
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg


@shared_task
def generate_daily_metrics():
    """Generate daily metrics for analytics"""
    yesterday = (timezone.now() - timedelta(days=1)).date()
    
    # Get alerts from yesterday
    alerts = Alert.objects.filter(
        detected_at__date=yesterday
    )
    
    # Calculate metrics
    metrics, created = DailyMetrics.objects.get_or_create(
        date=yesterday,
        defaults={
            'total_alerts': alerts.count(),
            'critical_alerts': alerts.filter(severity='CRITICAL').count(),
            'high_alerts': alerts.filter(severity='HIGH').count(),
            'medium_alerts': alerts.filter(severity='MEDIUM').count(),
            'low_alerts': alerts.filter(severity='LOW').count(),
            'resolved_alerts': alerts.filter(status='RESOLVED').count(),
            'false_positives': alerts.filter(status='FALSE_POSITIVE').count(),
        }
    )
    
    # Incident metrics
    incidents = Incident.objects.filter(detected_at__date=yesterday)
    metrics.total_incidents = incidents.count()
    metrics.open_incidents = incidents.filter(status='OPEN').count()
    metrics.closed_incidents = incidents.filter(status='CLOSED').count()
    
    # Playbook metrics
    executions = PlaybookExecution.objects.filter(created_at__date=yesterday)
    metrics.playbooks_executed = executions.count()
    metrics.playbooks_successful = executions.filter(status='SUCCESS').count()
    
    # Response time metrics (in seconds)
    resolved_alerts = alerts.filter(status='RESOLVED', time_to_resolve__isnull=False)
    if resolved_alerts.exists():
        metrics.avg_time_to_resolve = resolved_alerts.aggregate(
            avg=Avg('time_to_resolve')
        )['avg'].total_seconds()
    
    # Top MITRE techniques
    top_techniques = {}
    for alert in alerts:
        for technique in alert.mitre_techniques.all():
            key = f"{technique.technique_id} - {technique.name}"
            top_techniques[key] = top_techniques.get(key, 0) + 1
    
    metrics.top_mitre_techniques = dict(sorted(
        top_techniques.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10])
    
    # Top source IPs
    top_ips = {}
    for alert in alerts:
        if alert.source_ip:
            top_ips[str(alert.source_ip)] = top_ips.get(str(alert.source_ip), 0) + 1
    
    metrics.top_source_ips = dict(sorted(
        top_ips.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10])
    
    metrics.save()
    
    return f"Metrics generated for {yesterday}"