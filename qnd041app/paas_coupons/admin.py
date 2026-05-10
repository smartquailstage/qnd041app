from django.contrib import admin
from .models import Coupon
from unfold.admin import ModelAdmin

from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(ModelAdmin):

    # -------------------------------
    # List display
    # -------------------------------
    list_display = [
        'id',
        'code',
        'user',
        'credito',
        'percent_credit',
        'discount',
        'active',
        'valid_from',
        'valid_to',
        'created',
    ]

    # -------------------------------
    # Filters
    # -------------------------------
    list_filter = [
        'active',
        'credito',
        'valid_from',
        'valid_to',
        'created',
        'updated',
    ]

    # -------------------------------
    # Search
    # -------------------------------
    search_fields = [
        'code',
        'user__email',
        'user__username',
        'descripcion_valor_agregado',
    ]

    # -------------------------------
    # Readonly fields
    # -------------------------------
    readonly_fields = [
        'created',
        'updated',
    ]

    # -------------------------------
    # Ordering
    # -------------------------------
    ordering = ['-created']

    # -------------------------------
    # Fieldsets organizados en Tabs
    # -------------------------------
    fieldsets = (
        ('Información General', {
            'fields': (
                'user',
                'code',
                'active',
            ),
            'classes': ('unfold', 'tab-general'),
        }),

        ('Crédito y Descuentos', {
            'fields': (
                'credito',
                'percent_credit',
                'discount',
            ),
            'classes': ('unfold', 'tab-credit'),
        }),

        ('Vigencia del Cupón', {
            'fields': (
                'valid_from',
                'valid_to',
            ),
            'classes': ('unfold', 'tab-validity'),
        }),

        ('Información Financiera', {
            'fields': (
                'ingresos_anuales',
                'presupuesto_real',
            ),
            'classes': ('unfold', 'tab-finance'),
        }),

        ('Valor Agregado del Proyecto', {
            'fields': (
                'descripcion_valor_agregado',
            ),
            'classes': ('unfold', 'tab-project'),
        }),

        ('Fechas del Sistema', {
            'fields': (
                'created',
                'updated',
            ),
            'classes': ('unfold', 'tab-dates'),
        }),
    )

    # -------------------------------
    # Permite collapse/expand
    # -------------------------------
    unfold_fieldsets = True