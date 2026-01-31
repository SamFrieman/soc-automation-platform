from celery import shared_task
from alerts.models import Alert
from alerts.services import AlertClassifier
from playbooks.services import PlaybookOrchestrator
from django.utils import timezone
from datetime import timedelta


@shared_task
def process_alert(alert_id):
    """Process and classify an incoming alert"""
    try:
        alert = Alert.objects.get(id=alert_id)
        
        # Classify alert
        classifier = AlertClassifier()
        classification = classifier.classify_alert(alert)
        
        # Trigger playbooks
        orchestrator = PlaybookOrchestrator()
        orchestrator.trigger_playbooks(alert)
        
        return f"Alert {alert.alert_id} processed successfully"
    except Alert.DoesNotExist:
        return f"Alert {alert_id} not found"
    except Exception as e:
        return f"Error processing alert: {str(e)}"


@shared_task
def cleanup_old_alerts():
    """Clean up old resolved alerts"""
    from django.conf import settings
    
    cutoff_date = timezone.now() - timedelta(days=settings.ALERT_RETENTION_DAYS)
    
    old_alerts = Alert.objects.filter(
        status='RESOLVED',
        resolved_at__lt=cutoff_date
    )
    
    count = old_alerts.count()
    old_alerts.delete()
    
    return f"Deleted {count} old alerts"