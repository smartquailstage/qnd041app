import csv
import xlsxwriter
import datetime
from datetime import datetime
from django.contrib import admin
from .models import ServicioTerapeutico
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from usuarios.forms import ServicioTerapeuticoForm
from django.http import HttpResponse


def export_to_csv(modeladmin, request, queryset): 
    opts = modeladmin.model._meta 
    response = HttpResponse(content_type='text/csv') 
    response['Content-Disposition'] = 'attachment;' \
        'filename={}.csv'.format(opts.verbose_name) 
    writer = csv.writer(response) 
     
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many] 
    # Write a first row with header information 
    writer.writerow([field.verbose_name for field in fields]) 
    # Write data rows 
    for obj in queryset: 
        data_row = [] 
        for field in fields: 
            value = getattr(obj, field.name) 
            if isinstance(value, datetime): 
                value = value.strftime('%d/%m/%Y') 
            data_row.append(value) 
        writer.writerow(data_row) 
    return response 
export_to_csv.short_description = 'Export to CSV' 


def export_to_excel(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="{}.xlsx"'.format(opts.verbose_name_plural)

    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    # Obtener los campos del modelo
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # Escribir encabezados
    for i, field in enumerate(fields):
        worksheet.write(0, i, field.verbose_name)

    # Escribir datos
    for row_num, obj in enumerate(queryset, start=1):
        for col_num, field in enumerate(fields):
            value = getattr(obj, field.name)
            if isinstance(value, datetime):
                value = value.strftime('%d/%m/%Y')
            worksheet.write(row_num, col_num, str(value))  # Convertir a cadena de texto

    workbook.close()
    return response

export_to_excel.short_description = 'Exportar a Excel'




@admin.register(ServicioTerapeutico)
class ServicioTerapeuticoAdmin(ModelAdmin):
    list_display = ['servicio', 'costo_por_sesion','lugar_servicio', 'activo']
    list_editable = ['costo_por_sesion', 'activo']
    list_display_links = ['servicio']
    list_filter = ['activo','lugar_servicio']
    search_fields = ['servicio']
    list_per_page = 20
    actions = [export_to_csv, export_to_excel]



