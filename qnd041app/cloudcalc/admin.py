import csv
import xlsxwriter
from django.contrib import admin
from django.http import HttpResponse
from .models import Servicio, Estimacion
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from django.db import models
#from tabbed_admin import TabbedModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import path
from django.template.response import TemplateResponse
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.utils.html import format_html
from unfold.sections import TableSection, TemplateSection
#from .sites import custom_admin_site
from django.contrib.auth.admin import UserAdmin
from unfold.sites import UnfoldAdminSite
#from schedule.models import Calendar, Event, Rule, Occurrence
#from schedule.admin import CalendarAdmin 
from django.utils.timezone import localtime
from django.utils.timezone import make_aware
from django import forms
from django.utils import timezone
from unfold.components import BaseComponent, register_component
from unfold.sections import TableSection, TemplateSection
from django.utils.timezone import now

from django.template.loader import render_to_string
from unfold.decorators import action
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.html import format_html
from unfold.admin import StackedInline, TabularInline
from serviceapp.models import ServicioTerapeutico

from unfold.contrib.filters.admin import (
    AutocompleteSelectFilter,
    AutocompleteSelectMultipleFilter,
     RangeDateFilter, RangeDateTimeFilter
)
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
#from .widgets import CustomDatePickerWidget
from django.contrib.auth.admin import UserAdmin

from collections import defaultdict
from django.template.loader import render_to_string
from django.utils import timezone
from collections import defaultdict
from django.utils.timezone import localtime, is_naive, make_aware
from datetime import timedelta, time, date
from datetime import datetime
from django.contrib.auth import get_user_model



@admin.register(Servicio)
class ServicioAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_sheet = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    list_disable_select_all = False
    change_form_show_cancel_button = True

    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre', 'descripcion']



    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(Estimacion)
class EstimacionAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_sheet = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    list_disable_select_all = False
    change_form_show_cancel_button = True

    list_display = [
        'id', 'servicio', 'usuarios_estimados', 'tipo_uso',
        'proveedor', 'fecha', 'vcpu', 'ram_gb',
        'almacenamiento_gb', 'costo_estimado'
    ]

    list_filter = [
        'tipo_uso',
        'proveedor',
        'fecha',
        'servicio__nombre',
    ]

    search_fields = [
        'servicio__nombre',
        'tipo_uso',
        'proveedor',
    ]

    readonly_fields = ['fecha']



    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)