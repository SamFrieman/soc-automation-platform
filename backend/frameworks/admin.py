from django.contrib import admin
from .models import (
    MitreTactic, MitreTechnique, MitreSubTechnique,
    OwaspCategory, StrideCategory, KillChainStage,
    DiamondAdversary, DiamondInfrastructure, DiamondCapability, DiamondVictim
)

@admin.register(MitreTactic)
class MitreTacticAdmin(admin.ModelAdmin):
    list_display = ['tactic_id', 'name']
    search_fields = ['tactic_id', 'name']

@admin.register(MitreTechnique)
class MitreTechniqueAdmin(admin.ModelAdmin):
    list_display = ['technique_id', 'name']
    search_fields = ['technique_id', 'name']
    filter_horizontal = ['tactics']

@admin.register(MitreSubTechnique)
class MitreSubTechniqueAdmin(admin.ModelAdmin):
    list_display = ['sub_technique_id', 'name', 'parent_technique']
    search_fields = ['sub_technique_id', 'name']

@admin.register(OwaspCategory)
class OwaspCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'year', 'name', 'risk_rating']
    list_filter = ['year', 'risk_rating']
    search_fields = ['name']

@admin.register(StrideCategory)
class StrideCategoryAdmin(admin.ModelAdmin):
    list_display = ['stride_type', 'name']

@admin.register(KillChainStage)
class KillChainStageAdmin(admin.ModelAdmin):
    list_display = ['stage_number', 'name']
    ordering = ['stage_number']

@admin.register(DiamondAdversary)
class DiamondAdversaryAdmin(admin.ModelAdmin):
    list_display = ['name', 'sophistication_level', 'motivation', 'active']
    list_filter = ['sophistication_level', 'motivation', 'active']
    search_fields = ['name']

@admin.register(DiamondInfrastructure)
class DiamondInfrastructureAdmin(admin.ModelAdmin):
    list_display = ['infra_type', 'value', 'is_malicious', 'reputation_score']
    list_filter = ['infra_type', 'is_malicious']
    search_fields = ['value']

@admin.register(DiamondCapability)
class DiamondCapabilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'capability_type']
    list_filter = ['capability_type']
    search_fields = ['name']

@admin.register(DiamondVictim)
class DiamondVictimAdmin(admin.ModelAdmin):
    list_display = ['organization', 'industry', 'country']
    list_filter = ['industry']
    search_fields = ['organization']