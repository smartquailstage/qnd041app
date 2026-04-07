from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Contrato, ClausulaContrato
from django.utils.safestring import mark_safe
from django.urls import reverse


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
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'



def contract_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('smartcontracts:admin_contract_pdf', args=[obj.id])))
contract_pdf.short_description = 'Contrato'


from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr

class ClausulaContratoInline(TabularInline):
    model = ClausulaContrato
    extra = 1
    min_num = 0
    can_delete = True
    show_change_link = True

    fields = (
        'clausula',
        'titulo_clausura',
        'detalle',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            clausula_num=Cast(
                Substr('clausula', 10),  # Extrae el número después de "CLAUSULA_"
                IntegerField()
            )
        ).order_by('clausula_num')

@admin.register(Contrato)
class ContratoAdmin(ModelAdmin):

    search_fields = [
        'numero_contrato',
        'partes_contratantes',
        'objeto_contrato',
    ]

    list_display = [
        'numero_contrato',
        'tipo_contrato',
        'estado',
        'fecha_firma',
        contract_pdf,
    ]

    list_filter = [
        'tipo_contrato',
        'estado',
    ]

    list_fullwidth = True
    list_filter_sheet = True
    change_form_show_cancel_button = True
    warn_unsaved_form = True

    readonly_fields = [
        'created_at',
        'updated_at',
    ]

    editable_fields = [
        'created_at',
        'updated_at',
    ]
    # 🔹 Inline incluido
    inlines = [ClausulaContratoInline]

    fieldsets = (
        ('Información General del Contrato', {
            'fields': (
                'numero_contrato',
                'tipo_contrato',
                'estado',
                'contract_hash',
            ),
            'classes': ('unfold', 'tab-general'),
        }),
        ('Fechas del Contrato', {
            'fields': (
                'fecha_firma',
                'fecha_inicio',
                'fecha_fin',
            ),
            'classes': ('unfold', 'tab-fechas'),
        }),
        ('Partes y Objeto', {
            'fields': (
                'partes_contratantes',
                'cargo',
                'objeto_contrato',
            ),
            'classes': ('unfold', 'tab-contenido'),
        }),
        ('Observaciones y Auditoría', {
            'fields': (
                'observaciones',
                'created_at',
                'updated_at',
            ),
            'classes': ('unfold', 'tab-extra'),
        }),
    )

    unfold_fieldsets = True
