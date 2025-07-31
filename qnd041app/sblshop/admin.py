from django.contrib import admin
from .models import Category, SBLProduct
from parler.admin import TranslatableAdmin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SBLProduct)
class SBLProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
   # prepopulated_fields = {'slug': ('name',)}
    def get_populated_fields(self,request,obj=None):
        return {'slug': ('name',)}
