from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import BusinessProcess,BusinessSystemProject,BusinessAutomation,BusinessIntelligent,QATest,CloudResource


@admin.register(BusinessSystemProject)
class BusinessSystemProjectAdmin(ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    readonly_fields = ['created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description', 'user__username']







@admin.register(BusinessProcess)
class BusinessProcessAdmin(ModelAdmin):
    autocomplete_fields = ['project', 'assigned_developer']
    search_fields = ['name', 'project__name']
    list_display = [
        'name', 'project', 'assigned_developer', 'progress', 
        'has_automation', 'has_ai', 'approved_by_client'
    ]
    list_filter = [
        'has_automation', 'has_ai', 'approved_by_client', 
        'process_type', 'process_class', 'technology_type'
    ]
    list_fullwidth = True
    list_filter_sheet = True
    change_form_show_cancel_button = True
    warn_unsaved_form = True
    readonly_fields = ['total_development_days']

    # 🔹 Fieldsets completos con todos los campos y tabs
    fieldsets = (
        ('Información del Proceso de Negocio', {
            'fields': (
                'project', 'name', 'assigned_developer', 
                'description', 'numero_maximo_procesos', 
                'technology_type', 'progress'
            ),
            'classes': ('unfold', 'tab-general'),
        }),
        ('Fechas y Aprobación', {
            'fields': (
                'start_date', 'delivery_date', 
                'total_development_days', 'approved_by_client', 'final_url'
            ),
            'classes': ('unfold', 'tab-dates'),
        }),
        ('Clasificación', {
            'fields': (
                'process_type', 'process_class', 'process_event'
            ),
            'classes': ('unfold', 'tab-classification'),
        }),
        ('Automatización', {
            'fields': ('has_automation', 'automation_description'),
            'classes': ('unfold', 'tab-automation'),
        }),
        ('Inteligencia Artificial', {
            'fields': ('has_ai', 'ai_model_description'),
            'classes': ('unfold', 'tab-ai'),
        }),
    )

    # Permite expandir/collapse dentro de cada tab
    unfold_fieldsets = True



@admin.register(BusinessAutomation)
class BusinessAutomationAdmin(ModelAdmin):
    autocomplete_fields = ['project', 'assigned_developer']
    search_fields = ['name', 'project__name']
    list_display = [
        'name',
        'project',
        'assigned_developer',
        'automation_type',
        'progress',
        'start_date',
        'delivery_date',
        'approved_by_client',
        'total_development_days',
        'final_url'
    ]
    list_filter = [
        'automation_type',
        'approved_by_client',
        'start_date',
        'delivery_date'
    ]
    readonly_fields = ['total_development_days']
    change_form_show_cancel_button = True
    warn_unsaved_form = True
    list_fullwidth = True
    list_filter_sheet = True

    fieldsets = (
        ('📄 Información General', {
            'fields': (
                'project',
                'name',
                'description',
                'automation_type',
                'progress',
            ),
            'classes': ('collapse',),
        }),
        ('👤 Asignación Técnica', {
            'fields': (
                'assigned_developer',
            ),
            'classes': ('collapse',),
        }),
        ('📅 Fechas y Estado', {
            'fields': (
                'start_date',
                'delivery_date',
                'total_development_days',
                'approved_by_client',
            ),
            'classes': ('collapse',),
        }),
        ('🔗 Detalles Técnicos', {
            'fields': (
                'final_url',
            ),
            'classes': ('collapse',),
        }),
    )


# ⚙️ Admin para Inteligencia de Negocio
@admin.register(BusinessIntelligent)
class BusinessIntelligentAdmin(ModelAdmin):
    autocomplete_fields = ['project', 'assigned_developer']
    compressed_fields = True
    search_fields = ['name', 'project__name']
    list_display = ['name', 'project', 'assigned_developer', 'ai_type', 'progress', 'requires_gpu', 'approved_by_client']
    list_filter = ['ai_type', 'requires_gpu', 'approved_by_client']
    list_fullwidth = True
    list_filter_sheet = True
    change_form_show_cancel_button = True
    warn_unsaved_form = True
    readonly_fields = ['total_development_days']

    fieldsets = (
        ('Información de Inteligencia Artificial', {
            'fields': ('project', 'name', 'assigned_developer', 'description', 'ai_type', 'requires_gpu', 'progress'),
            'classes': ('collapse',),
        }),
        ('Fechas y Aprobación', {
            'fields': ('start_date', 'delivery_date', 'total_development_days', 'approved_by_client', 'final_url'),
            'classes': ('collapse',),
        }),
        ('Detalles Técnicos del Modelo', {
            'fields': ('model_accuracy', 'decision_maps', 'technical_notes'),
            'classes': ('collapse',),
        }),
    )


# 🧪 Admin para QA
@admin.register(QATest)
class QATestAdmin(ModelAdmin):
    autocomplete_fields = ['process']
    compressed_fields = True
    search_fields = ['test_case', 'process__name', 'executed_by']
    list_display = ['test_case', 'process', 'result', 'executed_by']
    list_filter = ['result', 'executed_at']
    editable_fields = ['result', 'description']
    readonly_fields = ("executed_at",)
    list_fullwidth = True
    list_filter_sheet = True
    change_form_show_cancel_button = True
    warn_unsaved_form = True

    fieldsets = (
        ('Prueba de Calidad QA', {
            'fields': (
                'process',
                'test_case',
                'description',
                'result',
                'executed_by',
            ),
            'classes': ('collapse',),
        }),
    )


# ☁️ Admin para Recursos en la Nube
@admin.register(CloudResource)
class CloudResourceAdmin(ModelAdmin):
    autocomplete_fields = ['project']
    compressed_fields = True
    search_fields = ['resource_name', 'provider']
    list_display = ['resource_name', 'provider', 'resource_type', 'monthly_cost_usd', 'monitoring_status']
    list_filter = ['provider', 'resource_type', 'monitoring_status']
    list_fullwidth = True
    list_filter_sheet = True
    change_form_show_cancel_button = True
    warn_unsaved_form = True

    fieldsets = (
        ('Recurso en la Nube', {
            'fields': (
                'project',
                'resource_name',
                'provider',
                'resource_type',
                'monthly_cost_usd',
            ),
            'classes': ('collapse',),
        }),
        ('Monitoreo y Alertas', {
            'fields': (
                'monitoring_tool',
                'monitoring_status',
                'alert_summary',
            ),
            'classes': ('collapse',),
        }),
    )
