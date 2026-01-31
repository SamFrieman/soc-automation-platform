from django.db import models
from django.contrib.auth.models import User
from alerts.models import Alert


class Incident(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('INVESTIGATING', 'Investigating'),
        ('CONTAINED', 'Contained'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]
    
    INCIDENT_TYPES = [
        ('MALWARE', 'Malware'),
        ('PHISHING', 'Phishing'),
        ('DATA_BREACH', 'Data Breach'),
        ('UNAUTHORIZED_ACCESS', 'Unauthorized Access'),
        ('DENIAL_OF_SERVICE', 'Denial of Service'),
        ('RANSOMWARE', 'Ransomware'),
        ('WEB_ATTACK', 'Web Attack'),
        ('OTHER', 'Other'),
    ]
    
    # Basic Information
    incident_id = models.CharField(max_length=100, unique=True, db_index=True)
    title = models.CharField(max_length=500)
    description = models.TextField()
    incident_type = models.CharField(max_length=30, choices=INCIDENT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    
    # Related Alerts
    alerts = models.ManyToManyField(Alert, related_name='incidents')
    
    # Assignment
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Impact
    affected_systems = models.JSONField(default=list, blank=True)
    affected_users = models.JSONField(default=list, blank=True)
    business_impact = models.TextField(blank=True)
    
    # Response
    containment_actions = models.TextField(blank=True)
    eradication_actions = models.TextField(blank=True)
    lessons_learned = models.TextField(blank=True)
    
    # Timestamps
    detected_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-detected_at']
    
    def __str__(self):
        return f"{self.incident_id} - {self.title}"