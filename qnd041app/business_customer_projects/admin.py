from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import BusinessProcess,BusinessSystemProject,BusinessAutomation,BusinessIntelligent,QATest,CloudResource


@admin.register(BusinessSystemProject)
class BusinessSystemProjectAdmin(ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    readonly_fields = ['created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description', 'user__username']





from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import BusinessProcess


@admin.register(BusinessProcess)
class BusinessProcessAdmin(ModelAdmin):

    autocomplete_fields = ['project', 'assigned_developer']
    search_fields = ['name', 'project__name']

    list_display = [
        'name',
        'project',
        'assigned_developer',
        'progress',
        'memory_percent_used',
        'cpu_percent_used',
        'storage_percent_used',
        'approved_by_client'
    ]

    list_filter = [
        'has_automation',
        'has_ai',
        'approved_by_client',
        'process_type',
        'process_class',
        'technology_type'
    ]

    readonly_fields = [
        'total_development_days',
        'memory_percent_used',
        'cpu_percent_used',
        'storage_percent_used'
    ]

    list_fullwidth = True
    list_filter_sheet = True
    change_form_show_cancel_button = True
    warn_unsaved_form = True

    fieldsets = (

        ("📌 Información general", {
            'fields': (
                'project',
                'name',
                'description',
                'numero_maximo_procesos',
                'process_type',
                'process_class',
                'technology_type',
                'process_event',
            )
        }),

        ("⚙️ Progreso y asignación", {
            'fields': (
                'progress',
                'assigned_developer',
                'approved_by_client',
            )
        }),

        ("🤖 Automatización e IA", {
            'fields': (
                'has_automation',
                'automation_description',
                'has_ai',
                'ai_model_description',
            )
        }),

        ("🖥️ Consumo de recursos", {
            'fields': (
                'memory_consumption',
                'cpu_consumption',
                'storage_consumption',
            )
        }),

        ("📊 Recursos disponibles", {
            'fields': (
                'total_memory_available',
                'total_cpu_available',

            )
        }),

        ("📈 Porcentajes (auto calculado)", {
            'fields': (
                'memory_percent_used',
                'cpu_percent_used',
                'storage_percent_used',
                'total_storage_available',
            )
        }),

        ("📅 Fechas", {
            'fields': (
                'start_date',
                'delivery_date',
                'total_development_days',
            )
        }),

        ("🌐 Entrega", {
            'fields': (
                'final_url',
            )
        }),
    )

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


from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import PaymentOrder



@admin.register(PaymentOrder)
class PaymentOrderAdmin(ModelAdmin):

    # Autocomplete si en un futuro agregas relaciones
    search_fields = [
        'user',
        'company_name',
        'company_ruc',
        'service_type',
    ]

    list_display = [
        'company_name',
        'company_ruc',
        'service_type',
        'cost',
        'iva',
        'cost_with_iva',
        'hourly_cost',
        'date_issued',
        'expiration_date',
        'second_expiration_date',
        'pago_verificado',
        'invoice_number',
    ]

    list_filter = [
        'service_type',
        'date_issued',
        'expiration_date',
        'pago_verificado',
    ]

    list_fullwidth = True
    list_filter_sheet = True
    warn_unsaved_form = True
    change_form_show_cancel_button = True

    readonly_fields = [
        'cost_with_iva',
        'hourly_cost',
        'second_expiration_date',
    ]

    # ──────────────────────────────────────────────
    # FIELDSETS CON TABS AL ESTILO BusinessProcessAdmin
    # ──────────────────────────────────────────────
    fieldsets = (

        ('🏢 Información de la Empresa', {
            'fields': (
                'user',
                'company_name',
                'company_ruc',
                'pago_verificado',
            ),
            'classes': ('unfold', 'tab-company'),
        }),

        ('💼 Información del Servicio', {
            'fields': (
                'project',
                'service_type',
                'cost',
                'iva',
                'cost_with_iva',
                'hourly_cost',
            ),
            'classes': ('unfold', 'tab-service'),
        }),

        ('📅 Fechas y Vigencias', {
            'fields': (
                'date_issued',
                'expiration_date',
                'second_expiration_date',
            ),
            'classes': ('unfold', 'tab-dates'),
        }),

        ('🧾 Facturación', {
            'fields': (
                'invoice_number',
                'invoice_file',
            ),
            'classes': ('unfold', 'tab-invoice'),
        }),

    )

    unfold_fieldsets = True




from .models import Noticia, ComentarioNoticia


class ComentarioNoticiaInline(admin.TabularInline):
    model = ComentarioNoticia
    extra = 0
    readonly_fields = ('usuario', 'fecha_creacion')
    fields = ('usuario', 'comentario', 'activo', 'fecha_creacion')



from .models import Noticia, NoticiaMetricas


class NoticiaMetricasInline(admin.StackedInline):
    model = NoticiaMetricas
    can_delete = False
    extra = 0
    verbose_name = "Métricas del Artículo"
    verbose_name_plural = "Métricas del Artículo"

    readonly_fields = (
        'ultima_actualizacion',
    )



@admin.register(Noticia)
class NoticiaAdmin(ModelAdmin):

    # ──────────────────────────────────────────────
    # BÚSQUEDA
    # ──────────────────────────────────────────────
    search_fields = [
        'titulo_1',
        'subtitulo_1',
        'autor_nombre',
    ]

    # ──────────────────────────────────────────────
    # LISTADO
    # ──────────────────────────────────────────────
    list_display = [
        'titulo_1',
        'autor_nombre',
        'fecha_publicacion',
        'activa',
    ]

    list_filter = [
        'activa',
        'fecha_publicacion',
        'autor_nombre',
    ]

    list_fullwidth = True
    list_filter_sheet = True
    warn_unsaved_form = True
    change_form_show_cancel_button = True

    inlines = [ComentarioNoticiaInline,NoticiaMetricasInline,]

    # ──────────────────────────────────────────────
    # SOLO LECTURA
    # ──────────────────────────────────────────────
    readonly_fields = [
        'fecha_publicacion',
    ]

    # ──────────────────────────────────────────────
    # FIELDSETS CON TABS (UNFOLD)
    # ──────────────────────────────────────────────
    fieldsets = (

        ('📰 Información Principal', {
            'fields': (
                'categoria',
                'titulo_1',
                'titulo_2',
                'titulo_3',
                'subtitulo_1',
                'subtitulo_2',
                'subtitulo_3',
            ),
            'classes': ('unfold', 'tab-main'),
        }),

        ('📄 Contenido de la Noticia', {
            'fields': (
                'cuerpo_1',
                'cuerpo_2',
                'cuerpo_3',
                'cuerpo_4',
                'cuerpo_5',
                'cuerpo_6',
                'cuerpo_7',
                'cuerpo_8',
                'cuerpo_9',
            ),
            'classes': ('unfold', 'tab-content'),
        }),

        ('🖼 Imágenes', {
            'fields': (
                'imagen_portada',
                'imagen_comercial',
                'imagen_datos_estadisticos',
            ),
            'classes': ('unfold', 'tab-images'),
        }),

        ('✍️ Autor', {
            'fields': (
                'autor_nombre',
                'autor_email',
                'autor_bio',
                'autor_foto',
            ),
            'classes': ('unfold', 'tab-author'),
        }),

        ('⚙️ Publicación', {
            'fields': (
                'refencia_1',
                'refencia_2',
                'refencia_3',
                'refencia_4',
                'activa',
                'fecha_publicacion',

            ),
            'classes': ('unfold', 'tab-publish'),
        }),

    )

    unfold_fieldsets = True


from .models import CategoriaNoticia


@admin.register(CategoriaNoticia)
class CategoriaNoticiaAdmin(ModelAdmin):

    list_display = ('nombre', 'slug', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre',)
    prepopulated_fields = {'slug': ('nombre',)}




from django.contrib import admin
from .models import SupportTicket

@admin.register(SupportTicket)
class SupportTicketAdmin(ModelAdmin):

    # ──────────────────────────────────────────────
    # Búsqueda
    # ──────────────────────────────────────────────
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'title',
        'description',
    ]

    # ──────────────────────────────────────────────
    # Listado
    # ──────────────────────────────────────────────
    list_display = [
        'title',
        'user',
        'consultation_type',
        'area',
        'question',
        'status',
        'scheduled_datetime',
        'created_at',
        'finished_at',
    ]

    list_filter = [
        'status',
        'consultation_type',
        'area',
        'scheduled_datetime',
        'created_at',
    ]

    list_fullwidth = True
    list_filter_sheet = True
    warn_unsaved_form = True
    change_form_show_cancel_button = True

    readonly_fields = [
        'created_at',
        'finished_at',
    ]

    # ──────────────────────────────────────────────
    # FIELDSETS CON TABS
    # ──────────────────────────────────────────────
    fieldsets = (

        ('👤 Usuario', {
            'fields': (
                'user',
            ),
            'classes': ('unfold', 'tab-user'),
        }),

        ('💻 Información de la Consulta', {
            'fields': (
                'title',
                'description',
                'consultation_type',
                'area',
                'question',
            ),
            'classes': ('unfold', 'tab-consultation'),
        }),

        ('📅 Programación', {
            'fields': (
                'scheduled_datetime',
                'status',
                'created_at',
                'finished_at',
            ),
            'classes': ('unfold', 'tab-dates'),
        }),

    )

    unfold_fieldsets = True



from .models import MonthlySystemMetrics

@admin.register(MonthlySystemMetrics)
class MonthlySystemMetricsAdmin(ModelAdmin):
    search_fields = [
        'project__name',  # Permite buscar por nombre del proyecto
    ]

    list_display = [
        'project',
        'date',
        'almacenamiento_gb',
        'memoria_gb',
        'procesamiento_millicore',
        'total_hours',
    ]

    list_filter = [
        'project',
        'date',
    ]

    readonly_fields = []  # Aquí puedes poner campos que solo quieras mostrar como lectura

    fieldsets = (
        ('📊 Métricas Mensuales', {
            'fields': (
                'project',
                'date',
                'almacenamiento_gb',
                'memoria_gb',
                'procesamiento_millicore',
            ),
        }),
    )
