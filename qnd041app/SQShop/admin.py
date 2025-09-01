from django.contrib import admin
from .models import Category, Product
from SQOrders.models import Order
from coupons.models import Coupon

from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db import models
#from parler.admin import TranslatableAdmin
#from wagtail_modeladmin.options import ModelAdmin, modeladmin_register,ModelAdminGroup
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from decimal import Decimal
from parler.admin import TranslatableAdmin


@admin.register(Category)
class CategoryAdminClass(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }
    list_filter_submit = False
    list_fullwidth = False
    list_filter_sheet = True
    list_horizontal_scrollbar_top = False
    list_disable_select_all = False
    actions_list = []
    actions_row = []
    actions_detail = []
    actions_submit_line = []
    change_form_show_cancel_button = True

    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
        # ArrayField: {"widget": ArrayWidget},  # Si usas ArrayField
    }








@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['id', 'name','software','plataforma', 'numero_procesos','latencia_aproximada','usuarios_simultaneos', 'price', 'available',]
    list_editable = ['available',]
    list_filter = ['available', 'category']
    search_fields = ['name', 'description', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    readonly_fields = [
        'costo_total_desarrollo',
        'costo_project_management',
        'margen_sq',
        'total',
        'total_iva',
        'costo_total_desarrollo_paas',
        'costo_total_implementacion_paas',
        'total_paas',
        'total_paas_iva',
        'costo_total_nube',
        'total_nube',
        'total_nube_iva',
        'total_arch',
        'total_arch_iva',
    ]

    fieldsets = (
        ('Información General', {
            'fields': (
                'name', 'slug', 'description', 'price', 'category', 'available', 'iva'
            )
        }),
        ('Items relacionados', {
            'fields': ('item1', 'item2', 'item3')
        }),
        ('Imágenes del Producto', {
            'fields': ('image', 'image_2', 'image_3')
        }),
        ('Procesos y Desarrollo', {
            'fields': (
                'numero_procesos',
                'tiempo_desarrollo',
                'costo_hora_desarrollo',
                'costo_total_desarrollo',
                'tiempo_implementacion',
                'costo_hora_implementacion',
                'costo_project_management',
                'margen_sq',
                'total',
                'total_iva',
            )
        }),
        ('Servicios PaaS (UI/UX)', {
            'fields': (
                'horas_desarrollo_paas',
                'costo_hora_desarrollo_paas',
                'costo_total_desarrollo_paas',
                'horas_implementacion_paas',
                'costo_hora_implementacion_paas',
                'costo_total_implementacion_paas',
                'margen_sq_paas',
                'total_paas',
                'total_paas_iva',
            )
        }),
        ('Servicios en la Nube', {
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
        ('Arquitectura y SRE', {
            'fields': (
                'tiempo_arquitectura',
                'costo_hora_arquitectura',
                'costo_sre',
                'margen_sq_arch',
                'total_arch',
                'total_arch_iva',
            )
        }),
        ('Características Técnicas', {
            'fields': (
                'software',
                'plataforma',
                'automatizacion',
                'inteligencia_artificial',
                'latencia_aproximada',
                'usuarios_simultaneos',
            )
        }),

    )
