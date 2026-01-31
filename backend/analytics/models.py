from django.db import models


class DailyMetrics(models.Model):
    date = models.DateField(unique=True, db_index=True)
    
    # Alert Metrics
    total_alerts = models.IntegerField(default=0)
    critical_alerts = models.IntegerField(default=0)
    high_alerts = models.IntegerField(default=0)
    medium_alerts = models.IntegerField(default=0)
    low_alerts = models.IntegerField(default=0)
    resolved_alerts = models.IntegerField(default=0)
    false_positives = models.IntegerField(default=0)
    
    # Incident Metrics
    total_incidents = models.IntegerField(default=0)
    open_incidents = models.IntegerField(default=0)
    closed_incidents = models.IntegerField(default=0)
    
    # Response Times (seconds)
    avg_time_to_detect = models.FloatField(null=True, blank=True)
    avg_time_to_respond = models.FloatField(null=True, blank=True)
    avg_time_to_resolve = models.FloatField(null=True, blank=True)
    
    # Playbook Metrics
    playbooks_executed = models.IntegerField(default=0)
    playbooks_successful = models.IntegerField(default=0)
    
    # Top Threats
    top_mitre_techniques = models.JSONField(default=dict, blank=True)
    top_source_ips = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Daily Metrics"
    
    def __str__(self):
        return f"Metrics for {self.date}"


class ThreatIntelligence(models.Model):
    IOC_TYPES = [
        ('IP', 'IP Address'),
        ('DOMAIN', 'Domain'),
        ('URL', 'URL'),
        ('HASH', 'File Hash'),
        ('EMAIL', 'Email'),
    ]
    
    ioc_type = models.CharField(max_length=20, choices=IOC_TYPES)
    ioc_value = models.CharField(max_length=500, db_index=True)
    threat_type = models.CharField(max_length=100)
    confidence_score = models.IntegerField()
    severity = models.CharField(max_length=20)
    source = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-last_seen']
        unique_together = ['ioc_type', 'ioc_value', 'source']
    
    def __str__(self):
        return f"{self.ioc_type}: {self.ioc_value}"