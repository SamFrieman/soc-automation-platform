from django.contrib import admin
from .models import DailyMetrics, ThreatIntelligence

@admin.register(DailyMetrics)
class DailyMetricsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_alerts', 'total_incidents', 'playbooks_executed']
    date_hierarchy = 'date'

@admin.register(ThreatIntelligence)
class ThreatIntelligenceAdmin(admin.ModelAdmin):
    list_display = ['ioc_type', 'ioc_value', 'threat_type', 'confidence_score', 'is_active']
    list_filter = ['ioc_type', 'threat_type', 'is_active']
    search_fields = ['ioc_value']