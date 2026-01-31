from django.db import models
from django.contrib.postgres.fields import ArrayField

# MITRE ATT&CK Models
class MitreTactic(models.Model):
    tactic_id = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['tactic_id']
    
    def __str__(self):
        return f"{self.tactic_id} - {self.name}"


class MitreTechnique(models.Model):
    technique_id = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    tactics = models.ManyToManyField(MitreTactic, related_name='techniques')
    url = models.URLField()
    platforms = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['technique_id']
    
    def __str__(self):
        return f"{self.technique_id} - {self.name}"


class MitreSubTechnique(models.Model):
    sub_technique_id = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    parent_technique = models.ForeignKey(MitreTechnique, on_delete=models.CASCADE, related_name='sub_techniques')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sub_technique_id']
    
    def __str__(self):
        return f"{self.sub_technique_id} - {self.name}"


# OWASP Top 10 Models
class OwaspCategory(models.Model):
    YEAR_CHOICES = [('2021', '2021'), ('2017', '2017')]
    RISK_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    
    category_id = models.CharField(max_length=10)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES)
    name = models.CharField(max_length=200)
    description = models.TextField()
    risk_rating = models.CharField(max_length=20, choices=RISK_CHOICES)
    remediation = models.TextField()
    cwe_mapping = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['category_id', 'year']
        ordering = ['year', 'category_id']
    
    def __str__(self):
        return f"OWASP {self.year} - {self.category_id}: {self.name}"


# STRIDE Models
class StrideCategory(models.Model):
    STRIDE_TYPES = [
        ('S', 'Spoofing'),
        ('T', 'Tampering'),
        ('R', 'Repudiation'),
        ('I', 'Information Disclosure'),
        ('D', 'Denial of Service'),
        ('E', 'Elevation of Privilege'),
    ]
    
    stride_type = models.CharField(max_length=1, choices=STRIDE_TYPES, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    examples = models.TextField()
    countermeasures = models.TextField()
    security_property = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['stride_type']
    
    def __str__(self):
        return f"{self.stride_type} - {self.name}"


# Cyber Kill Chain Models
class KillChainStage(models.Model):
    STAGE_CHOICES = [
        (1, 'Reconnaissance'),
        (2, 'Weaponization'),
        (3, 'Delivery'),
        (4, 'Exploitation'),
        (5, 'Installation'),
        (6, 'Command & Control'),
        (7, 'Actions on Objectives'),
    ]
    
    stage_number = models.IntegerField(choices=STAGE_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    indicators = models.TextField()
    defensive_actions = models.TextField()
    example_tools = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['stage_number']
    
    def __str__(self):
        return f"Stage {self.stage_number}: {self.name}"


# Diamond Model - Adversary
class DiamondAdversary(models.Model):
    SOPHISTICATION = [
        ('NOVICE', 'Novice'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
        ('EXPERT', 'Expert'),
        ('NATION_STATE', 'Nation State'),
    ]
    
    MOTIVATION = [
        ('FINANCIAL', 'Financial'),
        ('ESPIONAGE', 'Espionage'),
        ('DISRUPTION', 'Disruption'),
        ('IDEOLOGY', 'Ideological'),
        ('UNKNOWN', 'Unknown'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    aliases = models.JSONField(default=list, blank=True)
    country = models.CharField(max_length=100, blank=True)
    motivation = models.CharField(max_length=20, choices=MOTIVATION)
    sophistication_level = models.CharField(max_length=20, choices=SOPHISTICATION)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Diamond Adversaries"
    
    def __str__(self):
        return self.name


# Diamond Model - Infrastructure
class DiamondInfrastructure(models.Model):
    INFRA_TYPES = [
        ('IP', 'IP Address'),
        ('DOMAIN', 'Domain'),
        ('EMAIL', 'Email'),
        ('URL', 'URL'),
        ('SERVER', 'Server'),
    ]
    
    infra_type = models.CharField(max_length=10, choices=INFRA_TYPES)
    value = models.CharField(max_length=500, db_index=True)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    adversaries = models.ManyToManyField(DiamondAdversary, related_name='infrastructure', blank=True)
    is_malicious = models.BooleanField(default=False)
    reputation_score = models.IntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ['infra_type', 'value']
        verbose_name_plural = "Diamond Infrastructure"
    
    def __str__(self):
        return f"{self.infra_type}: {self.value}"


# Diamond Model - Capability
class DiamondCapability(models.Model):
    CAPABILITY_TYPES = [
        ('MALWARE', 'Malware'),
        ('EXPLOIT', 'Exploit'),
        ('TOOL', 'Tool'),
        ('TECHNIQUE', 'Technique'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    capability_type = models.CharField(max_length=20, choices=CAPABILITY_TYPES)
    description = models.TextField()
    mitre_techniques = models.ManyToManyField(MitreTechnique, related_name='capabilities', blank=True)
    adversaries = models.ManyToManyField(DiamondAdversary, related_name='capabilities', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Diamond Capabilities"
    
    def __str__(self):
        return self.name


# Diamond Model - Victim
class DiamondVictim(models.Model):
    INDUSTRY_CHOICES = [
        ('FINANCE', 'Financial Services'),
        ('HEALTHCARE', 'Healthcare'),
        ('TECHNOLOGY', 'Technology'),
        ('GOVERNMENT', 'Government'),
        ('EDUCATION', 'Education'),
        ('RETAIL', 'Retail'),
        ('OTHER', 'Other'),
    ]
    
    organization = models.CharField(max_length=200)
    industry = models.CharField(max_length=20, choices=INDUSTRY_CHOICES)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['organization']
        verbose_name_plural = "Diamond Victims"
    
    def __str__(self):
        return f"{self.organization} ({self.industry})"