from django.contrib import admin
from .models import Category, Product
from orders.models import Order
from coupons.models import Coupon
from parler.admin import TranslatableAdmin
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register,ModelAdminGroup





class CategoryAdmin(ModelAdmin):
    model = Category
    menu_label = 'Product Catalog'  # El nombre que aparece en el menú de administración
    menu_icon = 'edit'  # El ícono que aparece en el menú
    list_display = ('name', 'slug')  # Qué columnas se muestran en la lista
    search_fields = ('name',)  # Campos por los cuales se puede buscar
    add_to_settings_menu = True 
    menu_item_name = "Mi nombre de menú personalizado" 

class ProductAdmin(ModelAdmin):
    model = Product
    menu_label = 'Stock Product '  # El nombre que aparece en el menú de administración
    menu_icon = 'edit'  # El ícono que aparece en el menú
    list_display = ('name', 'slug')  # Qué columnas se muestran en la lista
    search_fields = ('name',)  # Campos por los cuales se puede buscar
    add_to_settings_menu = True 
    menu_item_name = "Mi nombre de menú personalizado" 

class OrderAdmin(ModelAdmin):
    model = Order
    menu_label = 'Orders Leads'  # El nombre que aparece en el menú de administración
    menu_icon = 'tasks'  # El ícono que aparece en el menú
    list_display = ('name', 'slug')  # Qué columnas se muestran en la lista
    search_fields = ('name',)  # Campos por los cuales se puede buscar
    add_to_settings_menu = True 
    menu_item_name = "Mi nombre de menú personalizado" 

class CouponAdmin(ModelAdmin):
    model = Coupon
    menu_label = 'Discount Cupons'  # El nombre que aparece en el menú de administración
    menu_icon = 'tag'  # El ícono que aparece en el menú
    list_display = ('name', 'slug')  # Qué columnas se muestran en la lista
    search_fields = ('name',)  # Campos por los cuales se puede buscar
    add_to_settings_menu = True 
    menu_item_name = "Mi nombre de menú personalizado" 
    

# Registra el modelo en Wagtail Admin



class LibraryGroup(ModelAdminGroup):
    menu_label = "E-Commerce"  # name of the group of ModelAdmins
    menu_icon = "globe"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (CategoryAdmin, ProductAdmin,OrderAdmin,CouponAdmin)

modeladmin_register(LibraryGroup)




@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
            return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price', 'created', 'updated']
   # list_filter = ['available', 'created', 'updated']
   # list_editable = ['price', 'available']

    def get_prepopulated_fields(self, request, obj=None):
            return {'slug': ('name',)}
