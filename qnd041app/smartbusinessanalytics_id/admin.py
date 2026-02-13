from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Ingreso
from django.template.loader import render_to_string
from unfold.components import BaseComponent, register_component

def REPORTE_MOVIMIENTO_FINANCIERO_PDF(obj):
    # Genera la URL del reporte PDF usando el reverse y el ID del objeto
    url = reverse("smartbusinessanalytics_id:pdf_reporte_movimiento_financiero", args=[obj.pk])
    
    # Retorna un enlace que abrirá el PDF en una nueva pestaña
    return mark_safe(
        f'<a href="{url}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span> '
        f'Reporte de Movimiento Financiero</a>'
    )

REPORTE_MOVIMIENTO_FINANCIERO_PDF.short_description = "Reporte de Movimiento Financiero"



import io
import base64
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime
from calendar import monthrange

from unfold.components import BaseComponent, register_component
from django.template.loader import render_to_string

from .models import MovimientoFinanciero


from django.db.models import Sum
from django.template.loader import render_to_string
from decimal import Decimal
from .models import MovimientoFinanciero


@register_component
class MovimientoFinancieroResumenComponent(BaseComponent):
    template_name = "admin/movimientos.html"
    name = "Resumen Movimiento Financiero"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):

        iva_ingresos = (
            MovimientoFinanciero.objects
            .filter(es_ingreso=True)
            .aggregate(total=Sum("iva"))["total"]
            or Decimal("0.00")
        )

        iva_egresos = (
            MovimientoFinanciero.objects
            .filter(es_egreso=True)
            .aggregate(total=Sum("iva"))["total"]
            or Decimal("0.00")
        )

        iva_por_pagar = iva_ingresos - iva_egresos

        cards = [
            {
                "title": "IVA Ingresos",
                "value": float(iva_ingresos),
                "badge": "USD",
                "badge_color": "success",
            },
            {
                "title": "IVA Egresos",
                "value": float(iva_egresos),
                "badge": "USD",
                "badge_color": "warning",
            },
            {
                "title": "IVA por Pagar",
                "value": float(iva_por_pagar),
                "badge": "USD",
                "badge_color": "success" if iva_por_pagar >= 0 else "danger",
                "footer": "Ingresos - Egresos",
            },
        ]

        return {
            "title": "Resumen IVA Global",
            "cards": cards,
        }

    def render(self):
        return render_to_string(
            self.template_name,
            self.get_context_data(),
            request=self.request
        )

from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import MovimientoFinanciero


@admin.register(MovimientoFinanciero)
class MovimientoFinancieroAdmin(ModelAdmin):
    # ----------------------------------
    # Componentes visuales
    # ----------------------------------
    list_sections = [
        MovimientoFinancieroResumenComponent,
    ]

    # ----------------------------------
    # Fieldsets en tabs
    # ----------------------------------
    fieldsets = (
        ("I. Información General", {
            "fields": (
                "es_ingreso",
                "es_egreso",
                "categoria_ingresos",
                "categoria",
                "fecha_devengo",
                "codigo_referencia",
                "descripcion",
                "contraparte_nombre",
                "contraparte_identificacion_fiscal",
                "confirmado",
            ),
            'classes': ('collapse',),
        }),

        ("II. Detalle", {
            "fields": (
                "monto_bruto",
                "descuento",
                "tasa_iva",
                "costo_directo",
                "gastos_indirectos",
            ),
           'classes': ('collapse',),
        }),

        ("IV. Resultados Calculados", {
            "fields": (
                "base_imponible",
                "iva",
                "monto_neto",
                "utilidad_bruta",
                "utilidad_neta",
            ),
         'classes': ('collapse',),
        }),

        ("V. Metadatos", {
            "fields": (
                "hash_registro",
                "created_at",
                "fecha_registro",
            ),
          'classes': ('collapse',),
        }),
    )

    # ----------------------------------
    # Listado en admin
    # ----------------------------------
    conditional_fields = {

    "categoria_ingresos": "es_ingreso",

    # Se muestra si es egreso
    "categoria": "es_egreso",
   
    }



    list_display = (
        "fecha_devengo",
        "tipo_movimiento",
        "categoria",
        "monto_principal",
        "utilidad_neta",
        "confirmado",
    )

    list_filter = (
        "es_ingreso",
        "es_egreso",
        "categoria",
        "fecha_devengo",
        "confirmado",
    )

    search_fields = (
        "codigo_referencia",
        "descripcion",
        "contraparte_nombre",
        "contraparte_identificacion_fiscal",
    )

    readonly_fields = (
        "hash_registro",
        "base_imponible",
        "iva",
        "monto_neto",
        "utilidad_bruta",
        "utilidad_neta",
        "created_at",
        "fecha_registro",
    )

    unfold_fieldsets = True

    # ----------------------------------
    # Campos calculados para listado
    # ----------------------------------
    def tipo_movimiento(self, obj):
        return "Ingreso" if obj.es_ingreso else "Egreso"
    tipo_movimiento.short_description = "Tipo"

    def monto_principal(self, obj):
        return obj.monto_neto
    monto_principal.short_description = "Monto Neto"

    # ----------------------------------
    # Media JS para ocultar tabs dinámicamente según tipo de movimiento
    # ----------------------------------
    class Media:
        js = ('admin/js/movimiento_financiero_toggle.js',)




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
from datetime import datetime, date
from calendar import monthrange
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from django.template.loader import render_to_string

import io
import base64
from datetime import datetime
from calendar import monthrange

import numpy as np
import matplotlib.pyplot as plt
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

import io
import base64
from datetime import datetime
from calendar import monthrange

import numpy as np
import matplotlib.pyplot as plt

from django.template.loader import render_to_string
from django.contrib import admin
from django.db.models import Sum



import io
import base64
from datetime import datetime
from calendar import monthrange

import numpy as np
import matplotlib.pyplot as plt

from django.template.loader import render_to_string
from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from calendar import monthrange
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from calendar import monthrange
from django.template.loader import render_to_string
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from calendar import monthrange
from django.template.loader import render_to_string

import io
import base64
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from calendar import monthrange
from django.template.loader import render_to_string
from unfold.components import BaseComponent, register_component
from .models import Ingreso, Egreso

import io
import base64
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from calendar import monthrange
from django.template.loader import render_to_string
from unfold.components import BaseComponent, register_component
from .models import Ingreso, Egreso
import io
import base64
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from calendar import monthrange
from django.template.loader import render_to_string
from unfold.components import BaseComponent, register_component
from .models import Ingreso, Egreso

from djmoney.money import Money

import io
import base64
from calendar import monthrange
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal
from djmoney.money import Money
from django.template.loader import render_to_string

from smartbusinessanalytics_id.models import MovimientoFinanciero, Ingreso, Egreso

@register_component
class EstadoResumenContableComponent(BaseComponent):
    template_name = "admin/banner.html"
    name = "Resumen Contable"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        e = self.instance

        # ==========================
        # Helper seguro
        # ==========================
        def money_to_float(m):
            return float(m.amount) if isinstance(m, Money) else float(m or 0.0)

        # ==========================
        # Tabla fechas
        # ==========================
        table_context = {
            "headers": ["Campo", "Detalle"],
            "rows": [
                ["Fecha inicio", e.fecha_inicio],
                ["Fecha fin", e.fecha_fin],
            ],
        }

        # ==========================
        # KPIs
        # ==========================
        cards = [
            {
            "title": "Efectivo Bancos",
            "value": e.total_efectivo_bancos, 
            "badge": f"Error: {e.error_conciliacion_porcentaje}%",
            "badge_color": "secondary","nombre_banco": e.nombre_banco, 
            "footer": f"Discrepancia: {e.diferencia_ingresos}"
            },

            {"title": "Punto de Equilibrio", "value": e.punto_equilibrio,
             "badge": f"Liquidez:{e.ratio_cobertura}%", "badge_color": "warning"},
            {"title": "Dividendos", "value": e.dividendos_accionistas, "badge": f"Rentabilidad: {e.rentabilidad}%", "badge_color": "success"},
        ]


        header_stats = [

        {
        "title": "Utilidades Netas",
        "value": e.utilidad_neta,
        "badge": "Utilidades",
        "badge_color": "sucess",
        "porcentaje": f"{e.margen_utilidad_neta}",
         },

        {
        "title": "Ingresos",
        "value": e.total_ingresos,
        "badge": "Ingresos",
        "badge_color": "primary",
        "discrepancia":f"{e.diferencia_ingresos}"
         },
         {
        "title": "Egresos",
        "value": e.total_egresos,
        "badge": "Egresos",
        "badge_color": "warning",
        "discrepancia": f"{ e.diferencia_egresos }"
         },
         {
        "title": "Fecha de inicio",
        "value": e.fecha_inicio,
        "badge": "Inicio",
        "badge_color": "success",
         },
         {
        "title": "Fecha de fin",
        "value": e.fecha_fin,
        "badge": "Fin",
        "badge_color": "success",
           },
         ]

        

        # ==========================
        # Lista de gastos
        # ==========================
        raw_gastos = [
            {"title": "Gastos Fijos", "value": e.gastos_fijos},
            {"title": "Gastos Operativos", "value": e.gastos_operativos},
            {"title": "Gastos Publicitarios", "value": e.gastos_publicitarios},
            {"title": "Gastos Legales", "value": e.gastos_legales},
            {"title": "Gastos Nómina", "value": e.gastos_nomina},
            {"title": "Gastos Tributarios", "value": e.gastos_tributarios},
            {"title": "Declaración IVA", "value": e.declaracion_iva},
            {"title": "Cuentas por Pagar", "value": e.cuentas_pagar},
            {"title": "Deudas", "value": e.deudas_pagar},
            
        ]

        raw_ingresos = [
            {"title": "Ventas", "value": e.ventas},
            {"title": "Inversiones", "value": e.inversiones},
            {"title": "Acciones Legales", "value": e.acciones_legales},
            {"title": "Cuentas por Cobrar", "value": e.cuentas_cobrar},
            {"title": "Deducción Gastos", "value": e.deduccion_gastos},
        ]

        # ==========================
        # Fechas
        # ==========================
        start = e.fecha_inicio
        end = e.fecha_fin
        if not start or not end:
            return {}

        if isinstance(start, datetime):
            start = start.date()
        if isinstance(end, datetime):
            end = end.date()

        # ==========================
        # Datos mensuales
        # ==========================
        months, ingresos, egresos, utilidades = [], [], [], []
        current = start.replace(day=1)

        while current <= end:
            months.append(current.strftime("%b %Y"))
            last_day = monthrange(current.year, current.month)[1]
            mes_inicio = current
            mes_fin = current.replace(day=last_day)

            ing = sum(
                money_to_float(i.monto_neto)
                for i in MovimientoFinanciero.objects.filter(fecha_devengo__range=(mes_inicio, mes_fin), es_ingreso=True)
            )
            egr = sum(
                money_to_float(x.monto_neto)
                for x in MovimientoFinanciero.objects.filter(fecha_devengo__range=(mes_inicio, mes_fin), es_egreso=True)
            )
            ingresos.append(ing)
            egresos.append(egr)
            utilidades.append(ing - egr)

            current = current.replace(
                year=current.year + (current.month // 12),
                month=(current.month % 12) + 1,
            )

        # ==========================
        # GRÁFICO 1 – BARRAS APILADAS
        # ==========================
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        x = np.arange(len(months))
        ax1.bar(x, ingresos,color=(111/255, 207/255, 151/255, 0.75))
        ax1.bar(x, egresos, bottom=ingresos,  color=(242/255, 201/255, 76/255, 0.65))
        ax1.bar(x, utilidades, bottom=np.array(ingresos)+np.array(egresos),
                 color=(79/255, 142/255, 247/255, 0.75) )
        ax1.set_xticks(x)
        ax1.set_xticklabels(months, rotation=45, ha="right")
        ax1.set_ylabel("USD")
        ax1.yaxis.grid(True, linestyle="--", alpha=0.4)
        ax1.set_axisbelow(True)
        ax1.legend()
        for spine in ax1.spines.values():
            spine.set_visible(False)
        buffer1 = io.BytesIO()
        fig1.savefig(buffer1, format="png", dpi=100, transparent=True, bbox_inches="tight")
        plt.close(fig1)
        buffer1.seek(0)
        bar_chart = f"data:image/png;base64,{base64.b64encode(buffer1.getvalue()).decode()}"

        # ==========================
        # GRÁFICO 2 – DISPERSIÓN
        # ==========================


        fig2, ax2, = plt.subplots(figsize=(6, 4))

        x_vals = np.array(ingresos)
        y_vals = np.array(egresos)
        # Valores bancarios
        x_bank = money_to_float(e.total_ingresos_bancos)
        y_bank = money_to_float(e.total_egresos_bancos)

# Error relativo = (bancos - contable) / contable
        # Error relativo pequeño para visualización
        x_err = np.array([abs(x_bank - x_vals[0]) * 0.5 if x_vals[0] != 0 else 0])
        y_err = np.array([abs(y_bank - y_vals[0]) * 0.5 if y_vals[0] != 0 else 0])



        ax2.errorbar(
            x_vals,
            y_vals,
            xerr=x_err,
            yerr=y_err,
            fmt="s",              # marcador cuadrado
            markersize=8,         # tamaño del rectángulo
            color="#e82b0c",
            ecolor="#e82b0c",
            elinewidth=2,
            capsize=6,
            alpha=0.85
            )


        if len(x_vals) > 1 and np.std(x_vals) > 0:
            m, b = np.polyfit(x_vals, y_vals, 1)
            ax2.plot(x_vals, m*x_vals+b, "--", color="gray", linewidth=3)
        ax2.set_xlabel("Ingresos (USD)")
        ax2.set_ylabel("Egresos (USD)")
        ax2.grid(True, linestyle="--", alpha=0.4)
        for spine in ax2.spines.values():
            spine.set_visible(False)
        buffer2 = io.BytesIO()
        fig2.savefig(buffer2, format="png", dpi=100, transparent=True, bbox_inches="tight")
        plt.close(fig2)
        buffer2.seek(0)
        scatter_chart = f"data:image/png;base64,{base64.b64encode(buffer2.getvalue()).decode()}"

  
       # ==========================
        # GRÁFICO 3 – PIE CHART por CATEGORIA
        # ==========================

        # ==========================
# Querysets base
# ==========================
        ingresos_qs = MovimientoFinanciero.objects.filter(
             fecha_devengo__range=(start, end),
             es_ingreso=True
        )

        egresos_qs = MovimientoFinanciero.objects.filter(
             fecha_devengo__range=(start, end),
              es_egreso=True
        )

        ingresos_categoria = {}
        for i in ingresos_qs:
            if i.categoria_ingresos:
                ingresos_categoria[i.categoria_ingresos] = (
                    ingresos_categoria.get(i.categoria_ingresos, 0)
                    + money_to_float(i.monto_neto)
                )

        egresos_categoria = {}
        for g in egresos_qs:
            if g.categoria:
                egresos_categoria[g.categoria] = (
                    egresos_categoria.get(g.categoria, 0)
                    + money_to_float(g.monto_neto)
                )

        ingresos_labels = list(ingresos_categoria.keys())
        ingresos_values = list(ingresos_categoria.values())

        egresos_labels = list(egresos_categoria.keys())
        egresos_values = list(egresos_categoria.values())

        fig3, (ax3, ax4) = plt.subplots(1, 2, figsize=(10, 5))

        if ingresos_values:
            ax3.pie(
                ingresos_values,
                labels=ingresos_labels,
                autopct="%1.1f%%",
                startangle=90,
                colors=plt.cm.Greens(np.linspace(0.4, 0.8, len(ingresos_labels)))
            )
           

        if egresos_values:
            ax4.pie(
                egresos_values,
                labels=egresos_labels,
                autopct="%1.1f%%",
                startangle=90,
                colors=plt.cm.YlOrBr(np.linspace(0.4, 0.8, len(egresos_labels)))
            )
          


        plt.tight_layout()
        buffer3 = io.BytesIO()
        fig3.savefig(buffer3, format="png", dpi=100, transparent=True, bbox_inches="tight")
        plt.close(fig3)
        buffer3.seek(0)

        pie_chart = f"data:image/png;base64,{base64.b64encode(buffer3.getvalue()).decode()}"


        # ==========================
        # CALCULAR PORCENTAJES DE GASTOS RELATIVOS A UTILIDAD NETA
        # ==========================
        ingresos_netos_float = money_to_float(e.total_ingresos)
        egresos_netos_float = money_to_float(e.total_egresos)
        utilidad_neta_float = money_to_float(e.utilidad_neta)

        gastos_valores = np.array([money_to_float(g["value"]) for g in raw_gastos], dtype=float)
        ingresos_valores = np.array([money_to_float(g["value"]) for g in raw_ingresos], dtype=float)

        if egresos_netos_float > 0:
            gastos_porcentajes = np.round((gastos_valores / egresos_netos_float ) * 100).astype(int)
        else:
            gastos_porcentajes = np.zeros_like(gastos_valores, dtype=int)

        if ingresos_netos_float > 0:
            ingresos_porcentajes = np.round((ingresos_valores / ingresos_netos_float ) * 100).astype(int)
        else:
            ingresos_porcentajes = np.zeros_like(ingresos_valores, dtype=int)



        gastos = []
        for g, pct in zip(raw_gastos, gastos_porcentajes):
            gastos.append({
                "title": g["title"],
                "value": money_to_float(g["value"]),
                "porcentaje_gasto": pct,  # listo para template
            })

        ingresos_corrientes = []
        for g, pct in zip(raw_ingresos, ingresos_porcentajes):
            ingresos_corrientes.append({
                "title": g["title"],
                "value": g["value"],
                "porcentaje_ingresos": pct,  # listo para template
            })

        # ==========================
        # CONTEXTO FINAL
        # ==========================
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Resumen Contable",
            "table": table_context,
            "header_stats": header_stats,
            "cards": cards,
            "gastos": gastos,
            "ingresos_corrientes": ingresos_corrientes,
            "chart_image": bar_chart,
            "scatter_chart_image": scatter_chart,
            "pie_chart_image": pie_chart,
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
            ["Liquidez (%)", e.ratio_cobertura],
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
        activos = e.analisis_flujo_financiero or {}
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





from .models import EstadoFinanciero

@admin.register(EstadoFinanciero)
class EstadoFinancieroAdmin(ModelAdmin):

    # ----------------------------------
    # Componentes visuales
    # ----------------------------------
    list_sections = [
        EstadoResumenContableComponent,
    ]

   
    # ----------------------------------
    # Fieldsets (tabs)
    # ----------------------------------
    fieldsets = (
        ("I. Crear Analítica", {
            
            "fields": ("nombre_banco","total_ingresos_bancos","total_egresos_bancos","fecha_inicio", "fecha_fin", 
            ),
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

        ("III. Detalle Egresos", {
            "fields": (
                "gastos_operativos",
                "gastos_nomina",
                "gastos_tributarios",
                "gastos_publicitarios",
                "gastos_legales",
                "declaracion_iva",
                "cuentas_pagar",
                "cuentas_cobrar",

            ),
            "classes": ("unfold", "tab-egresos"),
        }),



        ("IV. Detalle Ingresos", {
            "fields": (
                "ventas",
                "inversiones",
                "deduccion_gastos",
                "acciones_legales",
            ),
            "classes": ("unfold", "tab-ingresos"),
        }),


        ("V. Indicadores Financieros", {
            "fields": (
                "margen_utilidad_bruta",
                "margen_utilidad_neta",
                "rentabilidad",
                "ratio_cobertura",
            ),
            "classes": ("unfold", "tab-kpis"),
        }),

        ("VI. Análisis Avanzado (Flujo)", {
            "fields": (
                "punto_equilibrio",
                "dividendos_accionistas",
                "analisis_flujo_financiero",
            ),
            "classes": ("unfold", "tab-avanzado"),
        }),

        ("VII. Concliliación Bancaria", {
            "fields": (
               
                "total_efectivo_bancos",
                "total_efectivo",
                "diferencia_ingresos",
                "diferencia_egresos",
                "error_conciliacion_porcentaje",
                "umbral_conciliacion",
                "conciliado",

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
    )

    search_fields = ["nombre_banco",]

    list_filter = (
        "fecha_inicio",
        "fecha_fin",
    )

    search_fields = (
        "fecha_inicio",
        "fecha_fin",
    )

    # ----------------------------------
    # Campos solo lectura
    # ----------------------------------
    readonly_fields = (
        "total_ingresos",
        "total_egresos",
        "utilidad_bruta",
        "utilidad_neta",
        "margen_utilidad_bruta",
        "margen_utilidad_neta",
        "rentabilidad",
        "ratio_cobertura",
        "punto_equilibrio",
        "dividendos_accionistas",
        "analisis_flujo_financiero",
        "acciones_legales",
        "ventas",
        "inversiones",
        "gastos_operativos",
        "gastos_nomina",
        "gastos_tributarios",
        "gastos_publicitarios",
        "gastos_legales",
        "declaracion_iva",
        "deduccion_gastos",
        "cuentas_pagar",
        "cuentas_cobrar",
        "total_efectivo_bancos",
        "total_efectivo",
        "diferencia_ingresos",
        "diferencia_egresos",
        "error_conciliacion_porcentaje",
        "umbral_conciliacion",
      

    )

    unfold_fieldsets = True



from django.template.loader import render_to_string

from django.template.loader import render_to_string
from decimal import Decimal

@register_component
class ActivoPasivoResumenComponent(BaseComponent):
    template_name = "admin/activos_resumen.html"
    name = "Resumen Financiero"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        obj = self.instance

        if not obj:
            return {}

        def safe(v):
            return float(v) if v else 0.0

        context = super().get_context_data(**kwargs)

        # ===============================
        # ======== ACTIVO ==========
        # ===============================
        if obj.es_activo:

            cards = [
                {
                    "title": "Valor en Libros",
                    "value": safe(obj.net_book_value),
                    "badge": "USD",
                    "badge_color": "primary",
                },
                {
                    "title": "Costo Capitalizado",
                    "value": safe(obj.total_capitalized_cost),
                    "badge": "USD",
                    "badge_color": "success",
                },
                {
                    "title": "Depreciación Acumulada",
                    "value": safe(obj.depreciation_accumulated),
                    "badge": "USD",
                    "badge_color": "warning",
                },
                {
                    "title": "Acciones Equivalentes",
                    "value": safe(obj.shares_equivalent_nominal),
                    "badge": "ACC",
                    "badge_color": "success",
                },
                {
                    "title": "% Capital Social",
                    "value": safe(obj.percentage_of_share_capital),
                    "badge": "%",
                    "badge_color": "primary",
                },
            ]

            context.update({
                "title": "Resumen del Activo",
                "cards": cards,
                "tipo": "activo",
                "extra_data": {
                    "Capital Social": obj.total_share_capital,
                    "Total Acciones": obj.total_shares_issued,
                    "Valor Nominal Acción": obj.nominal_value_per_share,
                }
            })

        # ===============================
        # ======== PASIVO ==========
        # ===============================
        elif obj.es_pasivo:

            cards = [
                {
                    "title": "Saldo Pendiente",
                    "value": safe(obj.saldo_pendiente),
                    "badge": "USD",
                    "badge_color": "primary",
                },
                {
                    "title": "Interés Calculado",
                    "value": safe(obj.interes_calculado),
                    "badge": "USD",
                    "badge_color": "warning",
                },
                {
                    "title": "Total Adeudado",
                    "value": safe(obj.total_adeudado),
                    "badge": "USD",
                    "badge_color": "danger",
                },
                {
                    "title": "Acciones Potenciales",
                    "value": safe(obj.acciones_potenciales),
                    "badge": "ACC",
                    "badge_color": "success",
                },
                {
                    "title": "% Dilución Potencial",
                    "value": safe(obj.porcentaje_dilucion_potencial),
                    "badge": "%",
                    "badge_color": "warning",
                },
            ]

            context.update({
                "title": "Resumen del Pasivo",
                "cards": cards,
                "tipo": "pasivo",
                "extra_data": {
                    "Acreedor": obj.creditor,
                    "Fecha Vencimiento": obj.due_date,
                    "Tasa Interés": obj.interest_rate,
                }
            })

        else:
            return {}

        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import activos


@admin.register(activos)
class ActivosAdmin(ModelAdmin):

    # =============================
    # COMPONENTE VISUAL
    # =============================
    list_sections = [
        ActivoPasivoResumenComponent,
    ]

    # =============================
    # FIELDSETS
    # =============================
    fieldsets = (

        ("I. Tipo de Registro", {
            "fields": (
                "es_activo",
                "es_pasivo",
            ),
        }),

        # -----------------------------
        # ACTIVO
        # -----------------------------
        ("II. Información del Activo", {
            "fields": (
                "asset_code",
                "name",
                "description",
                "category",
                "serial_number",
                "brand",
                "model",
                "status",
            ),
            "classes": ("collapse",),
        }),

        ("III. Finanzas del Activo", {
            "fields": (
                "acquisition_date",
                "acquisition_cost",
                "additional_costs",
                "useful_life_years",
                "residual_value",
                "depreciation_accumulated",
                "book_value",
            ),
            "classes": ("collapse",),
        }),

        ("IV. Información Societaria Activo", {
            "fields": (
                "total_share_capital",
                "total_shares_issued",
                "nominal_value_per_share",
                "book_value_per_share",
                "market_value_per_share",
            ),
            "classes": ("collapse",),
        }),

        # -----------------------------
        # PASIVO
        # -----------------------------
        ("V. Información del Pasivo", {
            "fields": (
                "code",
                "liability_type",
                "origin_date",
                "due_date",
                "initial_amount",
                "payments_made",
                "interest_rate",
                "penalties",
                "financial_expenses",
                "creditor",
                "conversion_price",
            ),
            "classes": ("collapse",),
        }),

        ("VI. Metadatos", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

    unfold_fieldsets = True

    # =============================
    # CAMPOS CONDICIONALES
    # =============================
    conditional_fields = {
        "asset_code": "es_activo",
        "acquisition_cost": "es_activo",
        "code": "es_pasivo",
        "initial_amount": "es_pasivo",
    }

    # =============================
    # LIST DISPLAY
    # =============================
    list_display = (
        "tipo_registro",
        "nombre_display",
        "valor_display",
        "status_display",
    )

    list_filter = (
        "es_activo",
        "es_pasivo",
        "status",
        "liability_type",
    )

    search_fields = (
        "asset_code",
        "code",
        "name",
        "creditor",
    )

    readonly_fields = (
        "book_value",
        "created_at",
        "updated_at",
    )

    # =============================
    # MÉTODOS PARA LISTADO
    # =============================

    def tipo_registro(self, obj):
        if obj.es_activo:
            return "Activo"
        if obj.es_pasivo:
            return "Pasivo"
        return "-"
    tipo_registro.short_description = "Tipo"

    def nombre_display(self, obj):
        return obj.name or obj.asset_code or obj.code
    nombre_display.short_description = "Nombre"

    def valor_display(self, obj):
        if obj.es_activo:
            return obj.net_book_value
        if obj.es_pasivo:
            return obj.total_adeudado
        return "-"
    valor_display.short_description = "Valor"

    def status_display(self, obj):
        return obj.status
    status_display.short_description = "Estado"
