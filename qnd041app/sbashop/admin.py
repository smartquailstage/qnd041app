from django.contrib import admin
from .models import Category,SBAProduct
from unfold.decorators import action
from unfold.admin import ModelAdmin


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
    actions = [duplicar_mensajes,]
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SBAProduct)
class SBAProductAdmin(ModelAdmin):
    actions = [duplicar_productos,]
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
