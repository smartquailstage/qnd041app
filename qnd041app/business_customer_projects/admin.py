from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from .models import BusinessSystemProject, BusinessProcess, QATest, CloudResource
from usuarios.widgets import CustomDatePickerWidget  # si lo tienes
  # si usas filtros de fecha como en tu ejemplo

# 👤 Admin para Proyectos
@admin.register(BusinessSystemProject)
class BusinessSystemProjectAdmin(ModelAdmin):
    autocomplete_fields = ['user']
    compressed_fields = True
    search_fields = ['name', 'user__username']
    list_display = ['name', 'user', 'created_at']
    list_filter = ['created_at']
    list_fullwidth = True
    list_filter_sheet = True
    change_form_show_cancel_button = True
    warn_unsaved_form = True

    formfield_overrides = {
        models.DateField: {
            "widget": CustomDatePickerWidget(),
        },
    }

    fieldsets = (
        ('Información del Proyecto', {
            'fields': ('name', 'description', 'user','crew_members'),
            'classes': ('collapse',),
        }),
    )


# ⚙️ Admin para Procesos de Negocio
@admin.register(BusinessProcess)
class BusinessProcessAdmin(ModelAdmin):
    autocomplete_fields = ['project', 'assigned_developer']
    compressed_fields = True
    search_fields = ['name', 'project__name']
    list_display = ['name', 'project', 'assigned_developer', 'progress', 'has_automation', 'has_ai', 'approved_by_client']
    list_filter = ['has_automation', 'has_ai', 'approved_by_client', 'process_type', 'process_class']
    list_fullwidth = True
    list_filter_sheet = True
    change_form_show_cancel_button = True
    warn_unsaved_form = True
    readonly_fields = ['total_development_days']

    fieldsets = (
        ('Información del Proceso de Negocio', {
            'fields': ('project', 'name', 'assigned_developer','technology_type', 'description', 'progress'),
            'classes': ('collapse',),
        }),
        ('Fechas y Aprobación', {
            'fields': ('start_date', 'delivery_date', 'total_development_days', 'approved_by_client','final_url'),
            'classes': ('collapse',),
        }),
        ('Clasificación', {
            'fields': ('process_type', 'process_class'),
            'classes': ('collapse',),
        }),
        ('Automatización', {
            'fields': ('has_automation', 'automation_description'),
            'classes': ('collapse',),
        }),
        ('Inteligencia Artificial', {
            'fields': ('has_ai', 'ai_model_description'),
            'classes': ('collapse',),
        }),
    )



# 🧪 Admin para QA
@admin.register(QATest)
class QATestAdmin(ModelAdmin):
    autocomplete_fields = ['process']
    compressed_fields = True
    search_fields = ['test_case', 'process__name', 'executed_by']
    list_display = ['test_case', 'process', 'result', 'executed_at', 'executed_by']
    list_filter = ['result', 'executed_at']
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
                'executed_at',
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
