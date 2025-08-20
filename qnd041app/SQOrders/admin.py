from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ProductCalculation
from .models import InfrastructureQuote

@admin.register(InfrastructureQuote)
class InfraQuoteAdmin(ModelAdmin):
    list_display = ['infra_type', 'estimated_cost', 'created_at']
    list_filter = ['infra_type']
    search_fields = ['infra_type']

@admin.register(ProductCalculation)
class ProductCalculationAdmin(ModelAdmin):
    list_display = ('product', 'result_cost', 'created_at')
    list_filter = ('product', 'include_rd', 'include_ai', 'include_automation')
    search_fields = ('product',)
    ordering = ('-created_at',)