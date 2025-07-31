import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from .models import Coupon
from django.urls import reverse
from django.utils.safestring import mark_safe

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'valid_from',
                    'valid_to', 'discount', 'active']
