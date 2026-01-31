from django.contrib import admin
from .models import Incident

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ['incident_id', 'title', 'incident_type', 'severity', 'status', 'detected_at']
    list_filter = ['incident_type', 'severity', 'status']
    search_fields = ['incident_id', 'title']
    date_hierarchy = 'detected_at'
    filter_horizontal = ['alerts']