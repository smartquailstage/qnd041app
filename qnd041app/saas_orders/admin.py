import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from .models import SaaSOrder, SaaSOrderItem
from django.urls import reverse
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from unfold.components import BaseComponent, register_component
from unfold.sections import TableSection, TemplateSection

def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('saas_orders:admin_order_detail', args=[obj.id])))

 
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


class OrderItemInline(admin.TabularInline):
    model = SaaSOrderItem
    raw_id_fields = ['product']


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('saas_orders:admin_order_pdf', args=[obj.id])))
order_pdf.short_description = 'Invoice'



from unfold.components import BaseComponent, register_component
from django.template.loader import render_to_string
from .models import SaaSOrder
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Usa backend no-GUI seguro
import matplotlib.pyplot as plt
from django.core.cache import cache
import hashlib


# orders/admin_components.py (o donde lo estés organizando)
import base64
import io
from django.core.cache import cache
from django.template.loader import render_to_string
from unfold.components import BaseComponent, register_component
from .models import SaaSOrder

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Evita uso de GUI
import matplotlib.pyplot as plt
from django.utils.timezone import localtime



from collections import defaultdict
import itertools


@register_component
class DistribucionSemanalSaaSOrdenesComponent(BaseComponent):
    name = "Distribución semanal de órdenes"
    template_name = "admin/order_frecuencia_chart.html"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        cache_key = "grafico_frecuencia_ordenes_semanal_v2"

        imagen_base64 = cache.get(cache_key)
        if imagen_base64:
            return {
                "title": self.name,
                "grafico_base64": imagen_base64,
                "from_cache": True
            }

        # Obtener fechas
        fechas = list(SaaSOrder.objects.values_list("created", flat=True).order_by("created"))
        if not fechas:
            return {
                "title": self.name,
                "grafico_base64": None,
                "mensaje": "No hay órdenes registradas aún.",
            }

        # Convertir a localtime si es necesario (recomendado)
        fechas = [localtime(f) for f in fechas]

        # ----------- 1. Órdenes por semana -----------
        frecuencias_semanales = defaultdict(int)
        for fecha in fechas:
            iso_year, iso_week, _ = fecha.isocalendar()
            key = f"{iso_year}-W{iso_week:02d}"
            frecuencias_semanales[key] += 1

        semanas = sorted(frecuencias_semanales.keys())
        cantidades = [frecuencias_semanales[s] for s in semanas]

        # ----------- 2. Acumulado semanal -----------
        acumulado = list(itertools.accumulate(cantidades))

        # ----------- 3. Órdenes por día de la semana -----------
        dias_semana = defaultdict(int)
        for fecha in fechas:
            nombre_dia = fecha.strftime('%A')  # e.g., 'Monday'
            dias_semana[nombre_dia] += 1

        dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        cantidades_dia = [dias_semana[d] for d in dias_orden]

        # ----------- 4. Órdenes por hora del día -----------
        horas = defaultdict(int)
        for fecha in fechas:
            horas[fecha.hour] += 1
        horas_ordenadas = sorted(horas.keys())
        cantidades_hora = [horas[h] for h in horas_ordenadas]

        # ----------- Crear gráfico con subplots -----------
        fig, axs = plt.subplots(2, 2, figsize=(16, 8))
        plt.subplots_adjust(hspace=0.4, wspace=0.3)

        # Subplot 1: Órdenes por semana
        axs[0, 0].bar(semanas, cantidades, color='mediumseagreen', edgecolor='black')
        axs[0, 0].set_title("Órdenes por semana")
        axs[0, 0].tick_params(axis='x', rotation=45)

        # Subplot 2: Acumulado semanal
        axs[0, 1].plot(semanas, acumulado, marker='o', color='cornflowerblue')
        axs[0, 1].set_title("Órdenes acumuladas")
        axs[0, 1].tick_params(axis='x', rotation=45)

        # Subplot 3: Órdenes por día de la semana
        axs[1, 0].bar(dias_orden, cantidades_dia, color='darkorange')
        axs[1, 0].set_title("Órdenes por día de la semana")
        axs[1, 0].tick_params(axis='x', rotation=45)

        # Subplot 4: Órdenes por hora del día
        axs[1, 1].bar(horas_ordenadas, cantidades_hora, color='slateblue')
        axs[1, 1].set_title("Órdenes por hora del día")
        axs[1, 1].set_xticks(range(0, 24))
        axs[1, 1].set_xlim(-0.5, 23.5)

        # Guardar imagen
        buffer = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        imagen_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()

        cache.set(cache_key, imagen_base64, timeout=600)

        return {
            "title": self.name,
            "grafico_base64": imagen_base64,
            "from_cache": False
        }

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())




@register_component
class OrderSaaSDetailComponent(BaseComponent):
    template_name = "admin/order_summary_card.html"
    name = "Detalles de la Orden"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance  # instancia del modelo Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.instance

        if not order:
            context.update({
                "title": "Detalle de la Orden",
                "table": {
                    "headers": ["Sin datos disponibles"],
                    "rows": [["No se encontró la orden."]],
                }
            })
            return context

        headers = ["Campo", "Valor"]
        rows = [
            ["ID", order.id],
            ["Fecha", order.created.strftime("%d/%m/%Y %H:%M") if order.created else "N/A"],
            ["Cliente", order.first_name + " " + order.last_name if order.first_name else "N/A"],
            ["Email", order.email],
            ["Razon Solcail", order.razon_social or "N/A"],
            ["Estado de Pago", "Pagado" if order.paid else "Pendiente"],
            ["Total", f"${order.get_total_cost().amount:,.2f} {order.get_total_cost().currency}"],

            # añade más campos según tu modelo
        ]

        context.update({
            "title": f"Detalles de la Orden #{order.id}",
            "table": {
                "headers": headers,
                "rows": rows,
            }
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())





@admin.register(SaaSOrder)
class SaaSOrderAdmin(ModelAdmin):
    list_sections = [OrderSaaSDetailComponent,DistribucionSemanalSaaSOrdenesComponent]
    list_display = ['id', 'first_name', 'last_name', 'email',
            'ruc', 'razon_social','telefono','paid', order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]

    def utilidad_bruta_total_display(self, obj):
        return f"${obj.utilidad_bruta_total():,.2f}"
    utilidad_bruta_total_display.short_description = "Utilidad Bruta"

    def valor_deducible_iva_total_display(self, obj):
        return f"${obj.valor_deducible_iva_total():,.2f}"
    valor_deducible_iva_total_display.short_description = "Deducible IVA"

    def utilidad_liquida_total_display(self, obj):
        return f"${obj.utilidad_liquida_total():,.2f}"
    utilidad_liquida_total_display.short_description = "Utilidad Líquida"



