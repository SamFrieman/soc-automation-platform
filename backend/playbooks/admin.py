from django.contrib import admin
from .models import Playbook, PlaybookExecution

@admin.register(Playbook)
class PlaybookAdmin(admin.ModelAdmin):
    list_display = ['name', 'playbook_type', 'enabled', 'auto_execute', 'execution_count', 'success_rate']
    list_filter = ['playbook_type', 'enabled', 'auto_execute']
    search_fields = ['name', 'description']
    filter_horizontal = ['mitre_techniques', 'owasp_categories', 'stride_categories', 'kill_chain_stages']

@admin.register(PlaybookExecution)
class PlaybookExecutionAdmin(admin.ModelAdmin):
    list_display = ['playbook', 'alert', 'status', 'started_at', 'completed_at']
    list_filter = ['status', 'playbook']
    date_hierarchy = 'created_at'