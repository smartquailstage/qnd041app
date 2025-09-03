from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
    prepopulated_fields = {"slug": ("name",)}

    readonly_fields = [
        'created', 'updated',
        'price',
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
        'utilidad_bruta',
        'valor_deducible_iva',
        'utilidad_liquida',
    ]

    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'slug', 'description', 'category', 'available'),
            'classes': ('collapse',),
        }),
        ('Items', {
            'fields': ('item1', 'item2', 'item3'),
            'classes': ('collapse',),
        }),
        ('Imágenes', {
            'fields': ('image', 'image_2', 'image_3'),
            'classes': ('collapse',),
        }),
        ('Tiempos', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',),
        }),
        ('Características técnicas', {
            'fields': (
                'software',
                'numero_procesos',
                'automatizacion',
                'inteligencia_artificial',
                'latencia_aproximada',
                'usuarios_simultaneos',
            ),
            'classes': ('collapse',),
        }),
        ('Costos de desarrollo e implementación', {
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
            'classes': ('collapse',),
        }),
        ('Costos de nube', {
            'fields': (
                'costo_cpu_mes',
                'costo_bucket_mes',
                'costo_balanceador_mes',
                'costo_total_nube',
                'margen_sq_nube',
                'total_nube',
                'total_nube_iva',
            ),
            'classes': ('collapse',),
        }),
        ('Costos de arquitectura', {
            'fields': (
                'tiempo_arquitectura',
                'costo_hora_arquitectura',
                'costo_sre',
                'margen_sq_arch',
                'total_arch',
                'total_arch_iva',
            ),
            'classes': ('collapse',),
        }),
        ('Rentabilidad', {
            'fields': (
                'utilidad_bruta',
                'valor_deducible_iva',
                'inversion_marketing',
                'utilidad_liquida',
            ),
            'classes': ('collapse',),
        }),
        ('Resumen de precios', {
            'fields': ('price',),
            'classes': ('collapse',),
        }),
    )
