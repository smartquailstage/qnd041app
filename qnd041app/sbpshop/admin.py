import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from sbmorders.models import Order, OrderItem, BankTransfer
from .models import SBPStaffItem,SBPTechnologiesItem
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category,SBPProduct,SBPProductManual,ManualItem, SBPStaffItem,SBPTechnologiesItem




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
 

class SBPStaffItemInline(admin.TabularInline):
    model = SBPStaffItem

class SBPTechnologiesItemInline(admin.TabularInline):
    model = SBPTechnologiesItem


@admin.register(SBPProduct)
class SBMProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SBPStaffItemInline,SBPTechnologiesItemInline]




@admin.register(SBPTechnologiesItem)
class SBMTechnologiesItemAdmin(admin.ModelAdmin):
    list_display = ['id', ]

@admin.register(SBPStaffItem)
class SBMStaffItemAdmin(admin.ModelAdmin):
    list_display = ['id', ]
 
    




def manual_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('sbmshop:admin_product_manual_pdf', args=[obj.id])))
manual_pdf.short_description = 'Manual' 

class ManualItemInline(admin.TabularInline):
    model = ManualItem
 

@admin.register(SBPProductManual)
class SBPProductManualAdmin(admin.ModelAdmin):
    list_display = ['product', 'category',manual_pdf]
    inlines = [ManualItemInline]






