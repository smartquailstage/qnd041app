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
    readonly_fields = [
        'total_development_days', 
        'memory_consumption', 'cpu_consumption', 
        'total_memory_available', 'total_cpu_available',
        'memory_percent_used', 'cpu_percent_used'
    ]

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
        ('Recursos del Proceso', {
            'fields': (
                'memory_consumption', 'cpu_consumption',
                'total_memory_available', 'total_cpu_available',
                'memory_percent_used', 'cpu_percent_used'
            ),
            'classes': ('unfold', 'tab-resources'),
        }),
    )

    # Permite expandir/collapse dentro de cada tab
    unfold_fieldsets = True


from .models import BusinessContracts

@admin.register(BusinessContracts)
class BusinessContractsAdmin(ModelAdmin):
    
    autocomplete_fields = ['project']
    search_fields = ['titulo', 'project__name']
    
    list_display = [
        'titulo',
        'project',
        'get_tipo_display',
        'archivo_link',
        'created_at',
        'updated_at',
    ]
    
    list_filter = [
        'tipo',
        'project',
        'created_at',
        'updated_at',
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    change_form_show_cancel_button = True
    warn_unsaved_form = True
    list_fullwidth = True
    list_filter_sheet = True
    
    fieldsets = (
        ('📄 Información General', {
            'fields': (
                'project',
                'titulo',
                'tipo',
            ),
            'classes': ('tab-general',),
        }),
        ('📁 Archivo del Contrato', {
            'fields': (
                'archivo',
            ),
            'classes': ('tab-file',),
        }),
        ('⏱ Tiempos', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('tab-dates',),
        }),
    )
    
    def archivo_link(self, obj):
        if obj.archivo:
            return f"<a href='{obj.archivo.url}' target='_blank'>Descargar</a>"
        return "No disponible"
    archivo_link.allow_tags = True
    archivo_link.short_description = "Archivo"
    
    def get_tipo_display(self, obj):
        return obj.get_tipo_display()
    get_tipo_display.short_description = "Tipo de Contrato"


@admin.register(BusinessAutomation)
class BusinessAutomationAdmin(ModelAdmin):

    autocomplete_fields = ['project', 'assigned_developer']
    search_fields = ['title', 'project__name']
    
    list_display = [
        'title',
        'project',
        'automation_category',
        'automation_type',
        'microservice_type',
        'assigned_developer',
        'progress',
        'start_date',
        'delivery_date',
        'approved_by_client',
        'total_development_days',
        'final_url'
    ]

    list_filter = [
        'automation_category',
        'automation_type',
        'microservice_type',
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
                'title',
                'description',
                'automation_category',
                'automation_type',
                'microservice_type',
                'progress',
            ),
            'classes': ('tab-general',),
        }),

        ('👤 Asignación Técnica', {
            'fields': (
                'assigned_developer',
            ),
            'classes': ('tab-assignment',),
        }),

        ('📅 Fechas y Estado', {
            'fields': (
                'start_date',
                'delivery_date',
                'total_development_days',
                'approved_by_client',
            ),
            'classes': ('tab-dates',),
        }),

        ('🔗 Detalles Técnicos', {
            'fields': (
                'final_url',
            ),
            'classes': ('tab-technical',),
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
