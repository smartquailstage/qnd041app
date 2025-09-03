from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


from django.contrib import admin
from .models import Product


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
    ]


    fieldsets = (

        ('Información básica', {
            'fields': ('name', 'slug', 'description', 'category', 'available')
        }),
        ('Items', {
            'fields': ('item1', 'item2', 'item3'),
        }),
        ('Imágenes', {
            'fields': ('image', 'image_2', 'image_3'),
        }),
        ('Tiempos', {
            'fields': ('created', 'updated'),
        }),
        ('Características técnicas', {
            'fields': (
                'software',
                'numero_procesos',
                'automatizacion',
                'inteligencia_artificial',
                'latencia_aproximada',
                'usuarios_simultaneos',
            )
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
            )
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
            )
        }),
        ('Costos de arquitectura', {
            'fields': (
                'tiempo_arquitectura',
                'costo_hora_arquitectura',
                'costo_sre',
                'margen_sq_arch',
                'total_arch',
                'total_arch_iva',
            )
        }),
        ('Resumen de precios', {
            'fields': ('price',),
        }),
    )

