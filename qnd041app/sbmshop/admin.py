import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from sbmorders.models import Order, OrderItem, BankTransfer
from .models import SBMStaffItem,SBMTechnologiesItem
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category,SBMProduct,SBMProductManual,ManualItem, SBMStaffItem,SBMTechnologiesItem




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
 

class SBMStaffItemInline(admin.TabularInline):
    model = SBMStaffItem

class SBMTechnologiesItemInline(admin.TabularInline):
    model = SBMTechnologiesItem


@admin.register(SBMProduct)
class SBMProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SBMStaffItemInline,SBMTechnologiesItemInline]




@admin.register(SBMTechnologiesItem)
class SBMTechnologiesItemAdmin(admin.ModelAdmin):
    list_display = ['id', ]

@admin.register(SBMStaffItem)
class SBMStaffItemAdmin(admin.ModelAdmin):
    list_display = ['id', ]
 
    




def manual_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('sbmshop:admin_product_manual_pdf', args=[obj.id])))
manual_pdf.short_description = 'Manual' 

class ManualItemInline(admin.TabularInline):
    model = ManualItem
 

@admin.register(SBMProductManual)
class SBMProductManualAdmin(admin.ModelAdmin):
    list_display = ['product', 'category',manual_pdf]
    inlines = [ManualItemInline]






