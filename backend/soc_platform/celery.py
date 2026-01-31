import os
from celery import Celery
from celery.schedules import crontab

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soc_platform.settings')

app = Celery('soc_platform')

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'cleanup-old-alerts': {
        'task': 'alerts.tasks.cleanup_old_alerts',
        'schedule': crontab(hour=2, minute=0),  # 2 AM daily
    },
    'generate-daily-metrics': {
        'task': 'analytics.tasks.generate_daily_metrics',
        'schedule': crontab(hour=0, minute=30),  # 12:30 AM daily
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')