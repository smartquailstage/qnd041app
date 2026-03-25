from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product, Suite
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


@admin.register(Suite)
class SuiteAdmin(ModelAdmin):
    list_display = ['suite',]

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    actions = [duplicar_productos,]
    list_display = (
        'name',
        'category',
        'payment_method',
        'price',
        'available',
    )

   # autocomplete_fields = ('suite',)

    prepopulated_fields = {
        "slug": ("name",)
    }

    readonly_fields = [
        'created',
        'updated',

        'price',
        'price_amount',

        'costo_total_desarrollo',
        'costo_project_management',
        'margen_sq',
        'total',
        'total_iva',

        'costo_total_nube',
        'margen_sq_nube',
        'total_nube',
        'total_nube_iva',

        'margen_sq_arch',
        'total_arch',
        'total_arch_iva',

        'kushki_credit_cost',
        'kushki_debit_cost',

        'utilidad_bruta',
        'valor_deducible_iva',
        'utilidad_liquida',
    ]

    fieldsets = (
        (
            'Información básica',
            {
                'fields': (
                    'name',
                    'slug',
                    'suite',
                    'description',
                    'category',
                    'available',
                    'is_reaserch',
                    'is_automatitation',
                    'is_intelligent',
                ),
                'classes': ('tab', 'tab-general', 'active'),
            },
        ),
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
        (
            'Imágenes',
            {
                'fields': (
                    'image',
                    'image_2',
                    'image_3',
                ),
                'classes': ('tab', 'tab-imagenes'),
            },
        ),
        (
            'Características técnicas',
            {
                'fields': (
                    'os',
                    'gpu',
                    'cpu',
                    'almacenamiento',
                    'ancho_banda',
                    'memoria',
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
        (
            'Costos de desarrollo',
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
        (
            'Nube',
            {
                'fields': (
                    'costo_cpu_mes',
                    'costo_bucket_mes',
                    'costo_balanceador_mes',
                    'costo_total_nube',
                    'margen_sq_nube',
                    'total_nube',
                    'total_nube_iva',
                ),
                'classes': ('tab', 'tab-nube'),
            },
        ),
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
        (
            'Resumen de precios',
            {
                'fields': (
                    'price',
                ),
                'classes': ('tab', 'tab-precio'),
            },
        ),
    )
