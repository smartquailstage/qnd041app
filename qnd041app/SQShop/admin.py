from django.contrib import admin
from .models import Category, Product
from orders.models import Order
from coupons.models import Coupon

from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db import models
#from parler.admin import TranslatableAdmin
#from wagtail_modeladmin.options import ModelAdmin, modeladmin_register,ModelAdminGroup
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from decimal import Decimal



@admin.register(Category)
class CategoryAdminClass(ModelAdmin):
    # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    # Warn before leaving unsaved changes in changeform
    warn_unsaved_form = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }

    # Display submit button in filters
    list_filter_submit = False

    # Display changelist in fullwidth
    list_fullwidth = False

    # Set to False, to enable filter as "sidebar"
    list_filter_sheet = True

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail

    # Changeform templates (located inside the form)
    #change_form_before_template = "some/template.html"
    #change_form_after_template = "some/template.html"

    # Located outside of the form
    #change_form_outer_before_template = "some/template.html"
    #change_form_outer_after_template = "some/template.html"

    # Display cancel button in submit line in changeform
    change_form_show_cancel_button = True # show/hide cancel button in changeform, default: False

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        }
    } 





@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['id', 'name', 'numero_procesos', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    search_fields = ['name', 'description', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    readonly_fields = [
        'costo_total_desarrollo',
        'costo_project_management',
        'margen_sq',
        'total',
        'total_iva',
        'created',
        'updated',
        'creado',
        'actualizado'
    ]

    fieldsets = (
        ('Información General', {
            'fields': ('name', 'slug', 'description', 'price', 'category', 'available','iva')
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
        ('Servicios en la Nube', {
            'fields': (
                'cloud_service_shared',
                'latencia',
                'disponibilidad',
                'vcpu',
                'memoria_gb',
                'almacenamiento_gb',
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
                'tipo_arquitectura',
                'tiempo_arquitectura',
                'costo_hora_arquitectura',
                'costo_sre',
                'margen_sq_arch',
                'total_arch',
                'total_arch_iva',
            )
        }),
    )


    