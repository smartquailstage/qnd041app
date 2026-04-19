from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product
from unfold.decorators import action

@admin.action(description="Duplicar Categorias seleccionados")
def duplicar_mensajes(modeladmin, request, queryset):
    for category in queryset:
        category.pk = None  # Elimina la clave primaria para crear una nueva entrada
        category.slug = None
        category.save()


@admin.action(description="Duplicar Productos seleccionados")
def duplicar_productos(modeladmin, request, queryset):
    for product in queryset:
        product.pk = None  # Elimina la clave primaria para crear una nueva entrada
        product.slug = None
        product.save()

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    actions = [duplicar_mensajes,]


@admin.register(Product)
class ProductAdmin(ModelAdmin):

    list_display = (
        'name',
        'category',
        'payment_method',
        'price',
        'available',
    )

    actions = [duplicar_productos]

    prepopulated_fields = {
        "slug": ("name",)
    }

    readonly_fields = [
        'created',
        'updated',
        'total_tiempo',

        'price',
        'price_amount',

        # Desarrollo
        'costo_total_desarrollo',
        'costo_project_management',
        'margen_sq',
        'total',
        'total_iva',

        # Automatización
        'costo_total_n8n',
        'margen_sq_n8n',
        'total_n8n',
        'total_n8n_iva',

        # AI
        'costo_total_ml',
        'margen_sq_ml',
        'total_ml',
        'total_ml_iva',

        # Nube
        'costo_total_nube',
        'margen_sq_nube',
        'total_nube',
        'total_nube_iva',

        # Arquitectura
        'margen_sq_arch',
        'total_arch',
        'total_arch_iva',

        # Kushki
        'kushki_credit_cost',
        'kushki_debit_cost',

        # Rentabilidad
        'utilidad_bruta',
        'valor_deducible_iva',
        'utilidad_liquida',
    ]

    fieldsets = (

        # =========================
        # GENERAL
        # =========================
        (
            'Información básica',
            {
                'fields': (
                    'name',
                    'slug',
                    'description',
                    'category',
                    'available',

                    'is_reaserch',
                    'is_automatitation',
                    'is_intelligent',
                    'is_gpu',
                ),
                'classes': ('tab', 'tab-general', 'active'),
            },
        ),

        # =========================
        # ITEMS
        # =========================
        (
            'Items',
            {
                'fields': (
                    'item1',
                    'item2',
                    'item3',
                ),
                'classes': ('tab', 'tab-items'),
            },
        ),

        # =========================
        # IMÁGENES
        # =========================
        (
            'Imágenes',
            {
                'fields': (
                    'image',
                    'image_2',
                    'image_3',
                    'image_4',
                ),
                'classes': ('tab', 'tab-imagenes'),
            },
        ),

        # =========================
        # CARACTERÍSTICAS
        # =========================
        (
            'Características técnicas',
            {
                'fields': (
                    'os',
                    'gpu',
                    'cpu',
                    'memoria',
                    'almacenamiento',
                    'ancho_banda',

                    'software',
                    'numero_procesos',
                    'automatizacion',
                    'inteligencia_artificial',
                    'latencia_aproximada',
                    'usuarios_simultaneos',
                ),
                'classes': ('tab', 'tab-tecnica'),
            },
        ),

        # =========================
        # DESARROLLO (I+D)
        # =========================
        (
            'Desarrollo (I+D)',
            {
                'fields': (
                    'tiempo_desarrollo',
                    'costo_hora_desarrollo',
                    'costo_total_desarrollo',

                    'tiempo_implementacion',
                    'costo_hora_implementacion',
                    'costo_project_management',

                    'margen_sq',
                    'total',
                    'iva',
                    'total_iva',
                ),
                'classes': ('tab', 'tab-desarrollo'),
            },
        ),

        # =========================
        # AUTOMATIZACIÓN (+A)
        # =========================
        (
            'Automatización (+A)',
            {
                'fields': (
                    'tiempo_implementacion_a',
                    'costo_nodos',
                    'costo_orquestacion',
                    'costo_conectores_terceros',

                    'costo_total_n8n',
                    'margen_sq_n8n',
                    'total_n8n',
                    'total_n8n_iva',
                ),
                'classes': ('tab', 'tab-automatizacion'),
            },
        ),

        # =========================
        # INTELIGENCIA ARTIFICIAL (+AI)
        # =========================
        (
            'Inteligencia Artificial (+AI)',
            {
                'fields': (
                    'tiempo_implementacion_ai',
                    'costo_entrenamiento',
                    'costo_inferencia',
                    'costo_mantenimiento_ml',

                    'costo_total_ml',
                    'margen_sq_ml',
                    'total_ml',
                    'total_ml_iva',
                ),
                'classes': ('tab', 'tab-ai'),
            },
        ),

        # =========================
        # NUBE
        # =========================
        (
            'Infraestructura en la Nube',
            {
                'fields': (
                    'costo_cpu_mes',
                    'costo_memory_mes',
                    'costo_bucket_mes',
                    'costo_balanceador_mes',
                    'costo_gpu_mes',

                    'costo_total_nube',
                    'margen_sq_nube',
                    'total_nube',
                    'total_nube_iva',
                ),
                'classes': ('tab', 'tab-nube'),
            },
        ),

        # =========================
        # ARQUITECTURA
        # =========================
        (
            'Arquitectura',
            {
                'fields': (
                    'tiempo_arquitectura',
                    'costo_hora_arquitectura',
                    'costo_sre',

                    'margen_sq_arch',
                    'total_arch',
                    'total_arch_iva',
                ),
                'classes': ('tab', 'tab-arquitectura'),
            },
        ),

        # =========================
        # KUSHKI
        # =========================
        (
            'Pasarela de Pago (Kushki)',
            {
                'fields': (
                    'payment_method',

                    'kushki_credit_percentage',
                    'kushki_credit_fixed',
                    'kushki_credit_cost',

                    'kushki_debit_percentage',
                    'kushki_debit_fixed',
                    'kushki_debit_cost',
                ),
                'classes': ('tab', 'tab-kushki'),
            },
        ),

        # =========================
        # RENTABILIDAD
        # =========================
        (
            'Rentabilidad',
            {
                'fields': (
                    'utilidad_bruta',
                    'valor_deducible_iva',
                    'inversion_marketing',
                    'utilidad_liquida',
                ),
                'classes': ('tab', 'tab-rentabilidad'),
            },
        ),

        # =========================
        # TIEMPOS
        # =========================
        (
            'Tiempo de Entrega',
            {
                'fields': (
                    'total_tiempo',
                ),
                'classes': ('tab', 'tab-tiempo'),
            },
        ),

        # =========================
        # PRECIO FINAL
        # =========================
        (
            'Resumen de precios',
            {
                'fields': (
                    'price',
                    'price_amount',
                    'subtotal',
                ),
                'classes': ('tab', 'tab-precio'),
            },
        ),
    )
