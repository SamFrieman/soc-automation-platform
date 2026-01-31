from django.db import models
from django.contrib.auth.models import User
from frameworks.models import MitreTechnique, OwaspCategory, StrideCategory, KillChainStage
from alerts.models import Alert


class Playbook(models.Model):
    PLAYBOOK_TYPES = [
        ('DETECTION', 'Detection'),
        ('CONTAINMENT', 'Containment'),
        ('ERADICATION', 'Eradication'),
        ('RECOVERY', 'Recovery'),
        ('INVESTIGATION', 'Investigation'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    playbook_type = models.CharField(max_length=20, choices=PLAYBOOK_TYPES)
    
    # Triggers
    mitre_techniques = models.ManyToManyField(MitreTechnique, blank=True, related_name='playbooks')
    owasp_categories = models.ManyToManyField(OwaspCategory, blank=True, related_name='playbooks')
    stride_categories = models.ManyToManyField(StrideCategory, blank=True, related_name='playbooks')
    kill_chain_stages = models.ManyToManyField(KillChainStage, blank=True, related_name='playbooks')
    
    # Execution
    script_path = models.CharField(max_length=500)
    timeout_seconds = models.IntegerField(default=300)
    enabled = models.BooleanField(default=True)
    auto_execute = models.BooleanField(default=False)
    parameters = models.JSONField(default=dict, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Statistics
    execution_count = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    failure_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def success_rate(self):
        if self.execution_count == 0:
            return 0
        return (self.success_count / self.execution_count) * 100


class PlaybookExecution(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('TIMEOUT', 'Timeout'),
    ]
    
    playbook = models.ForeignKey(Playbook, on_delete=models.CASCADE, related_name='executions')
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='playbook_executions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Execution metadata
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    triggered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Results
    output = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    actions_taken = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.playbook.name} - {self.alert.alert_id}"