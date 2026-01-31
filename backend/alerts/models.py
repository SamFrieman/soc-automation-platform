from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from frameworks.models import (
    MitreTechnique, MitreSubTechnique, OwaspCategory, 
    StrideCategory, KillChainStage, DiamondAdversary,
    DiamondInfrastructure, DiamondCapability, DiamondVictim
)


class Alert(models.Model):
    SEVERITY_CHOICES = [
        ('INFO', 'Informational'),
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('INVESTIGATING', 'Investigating'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('FALSE_POSITIVE', 'False Positive'),
    ]
    
    # Basic Information
    alert_id = models.CharField(max_length=100, unique=True, db_index=True)
    title = models.CharField(max_length=500)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    
    # Source Information
    source_system = models.CharField(max_length=100)
    source_ip = models.GenericIPAddressField(null=True, blank=True)
    destination_ip = models.GenericIPAddressField(null=True, blank=True)
    affected_user = models.CharField(max_length=255, blank=True)
    affected_asset = models.CharField(max_length=255, blank=True)
    
    # Framework Mappings
    mitre_techniques = models.ManyToManyField(MitreTechnique, blank=True, related_name='alerts')
    mitre_sub_techniques = models.ManyToManyField(MitreSubTechnique, blank=True, related_name='alerts')
    owasp_categories = models.ManyToManyField(OwaspCategory, blank=True, related_name='alerts')
    stride_categories = models.ManyToManyField(StrideCategory, blank=True, related_name='alerts')
    kill_chain_stage = models.ForeignKey(KillChainStage, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Diamond Model
    diamond_adversary = models.ForeignKey(DiamondAdversary, on_delete=models.SET_NULL, null=True, blank=True)
    diamond_infrastructure = models.ManyToManyField(DiamondInfrastructure, blank=True)
    diamond_capability = models.ForeignKey(DiamondCapability, on_delete=models.SET_NULL, null=True, blank=True)
    diamond_victim = models.ForeignKey(DiamondVictim, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Assignment
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_alerts')
    
    # Timestamps
    detected_at = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Metrics
    time_to_detect = models.DurationField(null=True, blank=True)
    time_to_respond = models.DurationField(null=True, blank=True)
    time_to_resolve = models.DurationField(null=True, blank=True)
    
    # Additional Data
    raw_log = models.JSONField(default=dict, blank=True)
    indicators_of_compromise = models.JSONField(default=list, blank=True)
    enrichment_data = models.JSONField(default=dict, blank=True)
    tags = models.JSONField(default=list, blank=True)
    analyst_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-detected_at']
    
    def __str__(self):
        return f"{self.alert_id} - {self.title}"
    
    def save(self, *args, **kwargs):
        if self.status == 'RESOLVED' and self.resolved_at is None:
            self.resolved_at = timezone.now()
            if self.detected_at:
                self.time_to_resolve = self.resolved_at - self.detected_at
        super().save(*args, **kwargs)


class AlertComment(models.Model):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment on {self.alert.alert_id}"