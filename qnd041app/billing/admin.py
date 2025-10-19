# admin.py

from django.contrib import admin
from .models import Facturation
from unfold.admin import ModelAdmin

@admin.register(Facturation)
class FacturationAdmin(ModelAdmin):
    list_display = ('invoice_number', 'project', 'amount_with_tax', 'created_at')
    list_filter = ('project',)
    #search_fields = ('invoice_number', 'project__name', 'detail')
    #autocomplete_fields = ('project', 'concept')
