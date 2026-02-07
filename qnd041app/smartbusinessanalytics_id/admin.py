from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Ingreso
from django.template.loader import render_to_string
from unfold.components import BaseComponent, register_component



def REPORTE_INGRESO_PDF(obj):
    url = reverse("smartbusinessanalytics_id:pdf_reporte_ingreso", args=[obj.id])
    return mark_safe(
        f'<a href="{url}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span> '
        f'Reporte de Ingreso</a>'
    )


REPORTE_INGRESO_PDF.short_description = "Reporte de Ingreso"



@register_component
class IngresoIdentificacionComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Identificación del Ingreso"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        i = self.instance
        rows = [
            ["Código de referencia", i.codigo_referencia],
            ["Tipo de ingreso", i.get_tipo_ingreso_display()],
            ["Producto / Servicio", i.producto_servicio],
            ["Fecha de devengo", i.fecha_devengo],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Identificación del Ingreso",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())




@register_component
class ClienteIngresoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Cliente"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        i = self.instance
        rows = [
            ["Cliente", i.cliente_nombre],
            ["Identificación fiscal", i.cliente_identificacion_fiscal or "No registrada"],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Cliente",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class TributacionIngresoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Detalle Tributario"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        i = self.instance
        rows = [
            ["Monto bruto", i.monto_bruto],
            ["Descuento", i.descuento],
            ["Base imponible", i.base_imponible],
            ["Tasa IVA", f"{i.tasa_iva * 100}%"],
            ["IVA", i.iva],
            ["Monto neto", i.monto_neto],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Detalle Tributario",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class UtilidadesIngresoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Utilidades"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        i = self.instance
        rows = [
            ["Costo del producto", i.costo_producto],
            ["Gastos asociados", i.gastos_asociados],
            ["Utilidad bruta", i.utilidad_bruta],
            ["Utilidad neta", i.utilidad_neta],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Costos y Utilidades",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class CobroIngresoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Cobro"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        i = self.instance
        rows = [
            ["Método de pago", i.get_metodo_pago_display()],
            ["Cobrado", "Sí" if i.cobrado else "No"],
            ["Fecha de cobro", i.fecha_cobro or "Pendiente"],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Información Bancaria",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())




@admin.register(Ingreso)
class IngresoAdmin(ModelAdmin):

    # ----------------------------------
    # Componentes visuales
    # ----------------------------------
    list_sections = [
        IngresoIdentificacionComponent,
        ClienteIngresoComponent,
        TributacionIngresoComponent,
        UtilidadesIngresoComponent,
        CobroIngresoComponent,
    ]

    # ----------------------------------
    # Fieldsets (tabs)
    # ----------------------------------
    fieldsets = (

        ("I. Identificación del Ingreso", {
            "fields": (
                "codigo_referencia",
                "tipo_ingreso",
                "producto_servicio",
                "fecha_devengo",
            ),
            "classes": ("unfold", "tab-identificacion"),
        }),

        ("II. Cliente", {
            "fields": (
                "cliente_nombre",
                "cliente_identificacion_fiscal",
            ),
            "classes": ("unfold", "tab-cliente"),
        }),

        ("III. Detalle Tributario", {
            "fields": (
                "monto_bruto",
                "descuento",
                "tasa_iva",
                "base_imponible",
                "iva",
                "monto_neto",
            ),
            "classes": ("unfold", "tab-tributario"),
        }),

        ("IV. Costos y Utilidades", {
            "fields": (
                "costo_producto",
                "gastos_asociados",
                "utilidad_bruta",
                "utilidad_neta",
            ),
            "classes": ("unfold", "tab-utilidades"),
        }),

        ("V. Conciliacion Bancaria", {
            "fields": (
                "codigo_referencia_pago",
                "banco",
                "metodo_pago",
                "cobrado",
                "fecha_cobro",
            ),
            "classes": ("unfold", "tab-cobro"),
        }),
    )

    # ----------------------------------
    # Listado
    # ----------------------------------
    list_display = (
        "codigo_referencia",
        "cliente_nombre",
        "fecha_devengo",
        "monto_neto",
        "cobrado",
        REPORTE_INGRESO_PDF,
    )

    search_fields = (
        "codigo_referencia",
        "cliente_nombre",
    )

    list_filter = (
        "tipo_ingreso",
        "cobrado",
        "fecha_devengo",
    )

    readonly_fields = (
        "base_imponible",
        "iva",
        "monto_neto",
        "utilidad_bruta",
        "utilidad_neta",
    )

    unfold_fieldsets = True

#-------------EGRESOS------------------

@register_component
class EgresoIdentificacionComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Identificación del Egreso"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        e = self.instance
        rows = [
            ["Código de referencia", e.codigo_referencia],
            ["Tipo de egreso", e.get_tipo_egreso_display()],
            ["Concepto", e.concepto],
            ["Fecha de devengo", e.fecha_devengo],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Identificación del Egreso",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class ProveedorEgresoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Proveedor / Beneficiario"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        e = self.instance
        rows = [
            ["Nombre", e.proveedor_nombre],
            ["Identificación fiscal", e.proveedor_identificacion_fiscal or "No registrada"],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Proveedor / Beneficiario",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class TributacionEgresoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Detalle Tributario"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        e = self.instance
        rows = [
            ["Monto bruto", e.monto_bruto],
            ["Descuento", e.descuento],
            ["Base imponible", e.base_imponible],
            ["Tasa IVA", f"{e.tasa_iva * 100}%"],
            ["IVA", e.iva],
            ["Monto neto", e.monto_neto],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Detalle Tributario",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class CostosEgresoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Costos y Utilidades"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        e = self.instance
        rows = [
            ["Costo asociado", e.costo_asociado],
            ["Gastos adicionales", e.gastos_adicionales],
            ["Utilidad bruta", e.utilidad_bruta],
            ["Utilidad neta", e.utilidad_neta],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Costos y Utilidades",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class PagoEgresoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Pago"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        e = self.instance
        rows = [
            ["Método de pago", e.get_metodo_pago_display()],
            ["Pagado", "Sí" if e.pagado else "No"],
            ["Fecha de pago", e.fecha_pago or "Pendiente"],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Información de Pago",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())




from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Egreso


from django.utils.safestring import mark_safe
from django.urls import reverse

def REPORTE_EGRESO_PDF(obj):
    url = reverse("smartbusinessanalytics_id:pdf_reporte_egreso", args=[obj.id])
    return mark_safe(
        f'<a href="{url}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span> '
        f'Reporte de Egreso</a>'
    )

REPORTE_EGRESO_PDF.short_description = "Reporte de Egreso"






@admin.register(Egreso)
class EgresoAdmin(ModelAdmin):

    # ----------------------------------
    # Componentes visuales
    # ----------------------------------
    list_sections = [
        EgresoIdentificacionComponent,
        ProveedorEgresoComponent,
        TributacionEgresoComponent,
        CostosEgresoComponent,
        PagoEgresoComponent,
    ]

    # ----------------------------------
    # Fieldsets (tabs)
    # ----------------------------------
    fieldsets = (
        ("I. Identificación del Egreso", {
            "fields": (
                "codigo_referencia",
                "tipo_egreso",
                "concepto",
                "fecha_devengo",
            ),
            "classes": ("unfold", "tab-identificacion"),
        }),

        ("II. Proveedor / Beneficiario", {
            "fields": (
                "proveedor_nombre",
                "proveedor_identificacion_fiscal",
            ),
            "classes": ("unfold", "tab-proveedor"),
        }),

        ("III. Detalle Tributario", {
            "fields": (
                "monto_bruto",
                "descuento",
                "tasa_iva",
                "base_imponible",
                "iva",
                "monto_neto",
            ),
            "classes": ("unfold", "tab-tributario"),
        }),

        ("IV. Costos y Utilidades", {
            "fields": (
                "costo_asociado",
                "gastos_adicionales",
                "utilidad_bruta",
                "utilidad_neta",
            ),
            "classes": ("unfold", "tab-costos"),
        }),

        ("V. Pago", {
            "fields": (
                "metodo_pago",
                "pagado",
                "fecha_pago",
            ),
            "classes": ("unfold", "tab-pago"),
        }),
    )

    # ----------------------------------
    # Listado
    # ----------------------------------
    list_display = (
        "codigo_referencia",
        "proveedor_nombre",
        "fecha_devengo",
        "monto_neto",
        "pagado",
        REPORTE_EGRESO_PDF,
    )

    search_fields = (
        "codigo_referencia",
        "proveedor_nombre",
    )

    list_filter = (
        "tipo_egreso",
        "pagado",
        "fecha_devengo",
    )

    readonly_fields = (
        "base_imponible",
        "iva",
        "monto_neto",
        "utilidad_bruta",
        "utilidad_neta",
    )

    unfold_fieldsets = True



from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from unfold.admin import ModelAdmin
from .models import EstadoFinanciero



# ================================
# Objeto PDF para Admin
# ================================
def REPORTE_FINANCIERO_PDF(obj):
    url = reverse("smartbusinessanalytics_id:pdf_reporte_financiero", args=[obj.id])
    return mark_safe(
        f'<a href="{url}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span> '
        f'Reporte Financiero</a>'
    )

REPORTE_FINANCIERO_PDF.short_description = "Reporte Financiero"



@register_component
class EstadoPeriodoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Período Analizado"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        e = self.instance
        rows = [
            ["Fecha inicio", e.fecha_inicio],
            ["Fecha fin", e.fecha_fin],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Período Financiero",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows},
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())

import json
from datetime import datetime
from django.template.loader import render_to_string



import io
import base64
from datetime import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")  # <- importante para que funcione en servidor
import matplotlib.pyplot as plt

from django.template.loader import render_to_string



@register_component
class EstadoResumenContableComponent(BaseComponent):
    template_name = "admin/banner.html"
    name = "Resumen Contable"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        e = self.instance

        # --------------------------
        # Tarjetas KPI
        # --------------------------
        cards = [
            {
                "title": "Total Ingresos",
                "value": e.total_ingresos,
                "badge": "Período",
                "badge_color": "primary",
                "footer": "+ ingresos generados",
            },
            {
                "title": "Total Egresos",
                "value": e.total_egresos,
                "badge": "Período",
                "badge_color": "warning",
                "footer": "+ costos incurridos",
            },
            {
                "title": "Utilidad Neta",
                "value": e.utilidad_neta,
                "badge": "Resultado",
                "badge_color": "success",
                "footer": "resultado final",
            },
        ]

        # --------------------------
        # Datos del gráfico por mes
        # --------------------------
        start = e.fecha_inicio
        end = e.fecha_fin

        if isinstance(start, datetime):
            start = start.date()
        if isinstance(end, datetime):
            end = end.date()

        months = []
        ingresos = []
        egresos = []

        current = start.replace(day=1)
        while current <= end:
            months.append(current.strftime("%b %Y"))

            # obtener valores por mes
            ingresos.append(getattr(e, "ingresos_por_mes", lambda d: 0)(current))
            egresos.append(getattr(e, "egresos_por_mes", lambda d: 0)(current))

            # siguiente mes
            next_month = current.month + 1
            next_year = current.year
            if next_month > 12:
                next_month = 1
                next_year += 1
            current = current.replace(year=next_year, month=next_month)

        # --------------------------
        # Crear gráfico con Matplotlib
        # --------------------------
        fig, ax = plt.subplots(figsize=(8, 4))
        x = np.arange(len(months))
        width = 0.4

        ax.bar(x - width/2, ingresos, width=width, label="Ingresos", color="#1D4ED8")  # azul
        ax.bar(x + width/2, egresos, width=width, label="Egresos", color="#F59E0B")      # amarillo

        ax.set_xticks(x)
        ax.set_xticklabels(months, rotation=45, ha="right")
        ax.set_ylabel("Monto")
        ax.set_title("Ingresos vs Egresos por Mes")
        ax.legend()
        plt.tight_layout()

        # Convertir figura a base64
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        chart_image = f"data:image/png;base64,{image_base64}"

        # --------------------------
        # Contexto
        # --------------------------
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Resumen Contable",
            "cards": cards,
            "chart_image": chart_image,
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())





@register_component
class EstadoKPIsComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Indicadores Financieros"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        e = self.instance
        rows = [
            ["Margen utilidad bruta (%)", e.margen_utilidad_bruta],
            ["Margen utilidad neta (%)", e.margen_utilidad_neta],
            ["Rentabilidad (%)", e.rentabilidad],
            ["Liquidez (%)", e.liquidez],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "KPIs Financieros",
            "table": {"headers": ["Indicador", "Valor"], "rows": rows},
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class EstadoAnalisisAvanzadoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Análisis Avanzado"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        e = self.instance
        activos = e.analisis_activos or {}
        rows = [
            ["Punto de equilibrio", e.punto_equilibrio],
            ["Dividendos a accionistas", e.dividendos_accionistas],
            ["Activos totales", activos.get("activos_totales", "—")],
            ["Liquidez sobre activos (%)", activos.get("proporcion_liquidez", "—")],
            ["Egresos sobre activos (%)", activos.get("proporcion_egresos", "—")],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Análisis Financiero Avanzado",
            "table": {"headers": ["Métrica", "Resultado"], "rows": rows},
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())



@admin.register(EstadoFinanciero)
class EstadoFinancieroAdmin(ModelAdmin):

    # ----------------------------------
    # Componentes visuales
    # ----------------------------------
    list_sections = [
        EstadoPeriodoComponent,
        EstadoResumenContableComponent,
        EstadoKPIsComponent,
        EstadoAnalisisAvanzadoComponent,
    ]

    # ----------------------------------
    # Fieldsets (tabs)
    # ----------------------------------
    fieldsets = (
        ("I. Período", {
            "fields": ("fecha_inicio", "fecha_fin"),
            "classes": ("unfold", "tab-periodo"),
        }),

        ("II. Resumen Contable", {
            "fields": (
                "total_ingresos",
                "total_egresos",
                "utilidad_bruta",
                "utilidad_neta",
            ),
            "classes": ("unfold", "tab-resumen"),
        }),

        ("III. Indicadores Financieros", {
            "fields": (
                "margen_utilidad_bruta",
                "margen_utilidad_neta",
                "rentabilidad",
                "liquidez",
            ),
            "classes": ("unfold", "tab-kpis"),
        }),

        ("IV. Análisis Avanzado", {
            "fields": (
                "punto_equilibrio",
                "dividendos_accionistas",
                "analisis_activos",
            ),
            "classes": ("unfold", "tab-avanzado"),
        }),
    )

    # ----------------------------------
    # Listado
    # ----------------------------------
    list_display = (
        "fecha_inicio",
        "fecha_fin",
        "total_ingresos",
        "total_egresos",
        "utilidad_neta",
    )

    list_filter = (
        "fecha_inicio",
        "fecha_fin",
    )

    search_fields = (
        "fecha_inicio",
        "fecha_fin",
    )

    readonly_fields = (
        "total_ingresos",
        "total_egresos",
        "utilidad_bruta",
        "utilidad_neta",
        "margen_utilidad_bruta",
        "margen_utilidad_neta",
        "rentabilidad",
        "liquidez",
        "punto_equilibrio",
        "dividendos_accionistas",
        "analisis_activos",
    )

    unfold_fieldsets = True
