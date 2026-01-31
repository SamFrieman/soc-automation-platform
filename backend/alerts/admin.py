from django.contrib import admin
from .models import Alert, AlertComment

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['alert_id', 'title', 'severity', 'status', 'detected_at']
    list_filter = ['severity', 'status', 'source_system']
    search_fields = ['alert_id', 'title', 'description']
    date_hierarchy = 'detected_at'
    filter_horizontal = ['mitre_techniques', 'owasp_categories', 'stride_categories']

@admin.register(AlertComment)
class AlertCommentAdmin(admin.ModelAdmin):
    list_display = ['alert', 'user', 'created_at']
    list_filter = ['created_at']