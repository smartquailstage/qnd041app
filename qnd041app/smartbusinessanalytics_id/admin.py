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


from django.template.loader import render_to_string
from .models import MovimientoFinanciero

@register_component
class MovimientoFinancieroResumenComponent(BaseComponent):
    template_name = "admin/movimientos.html"
    name = "Resumen Movimiento Financiero"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        obj = self.instance

        # ==========================
        # Helper seguro
        # ==========================
        def money(m):
            return float(m.amount) if m else 0.0

        # ==========================
        # Validación básica
        # ==========================
        if not obj:
            return {}

        # ==========================
        # Datos principales según tipo
        # ==========================
        ingreso = obj.es_ingreso
        egreso = obj.es_egreso

        # Montos principales
        total_ingresos = money(obj.monto_neto) if ingreso else 0
        total_egresos = money(obj.monto_neto) if egreso else 0
        utilidad = money(obj.utilidad_neta)

        # ==========================
        # Cards para mostrar
        # ==========================
        cards = []

        if ingreso:
            cards.append({
                "title": "Ingreso",
                "value": total_ingresos,
                "badge": "USD",
                "badge_color": "success",
            })

        if egreso:
            cards.append({
                "title": "Egreso",
                "value": total_egresos,
                "badge": "USD",
                "badge_color": "warning",
            })

        cards.append({
            "title": "Utilidad Neta",
            "value": utilidad,
            "badge": "USD",
            "badge_color": "primary",
        })

        # ==========================
        # Contexto final
        # ==========================
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Resumen Movimiento Financiero",
            "cards": cards,
            # No gráficos en esta versión
        })

        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())



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
                "fecha_devengo",
                "codigo_referencia",
                "descripcion",
                "categoria",
                "categoria_ingresos",
                "es_ingreso",
                "es_egreso",
                "contraparte_nombre",
                "contraparte_identificacion_fiscal",
                "confirmado",
            ),
            "classes": ("unfold", "tab-general"),
        }),

        ("II. Detalle", {
            "fields": (
                "monto_bruto",
                "descuento",
                "tasa_iva",
                "costo_directo",
                "gastos_indirectos",
            ),
            "classes": ("unfold", "tab-egreso"),
        }),

        ("IV. Resultados Calculados", {
            "fields": (
                "base_imponible",
                "iva",
                "monto_neto",
                "utilidad_bruta",
                "utilidad_neta",
            ),
            "classes": ("unfold", "tab-resultados"),
        }),

        ("V. Metadatos", {
            "fields": (
                "hash_registro",
                "created_at",
                "fecha_registro",
            ),
            "classes": ("unfold", "tab-meta"),
        }),
    )

    # ----------------------------------
    # Listado en admin
    # ----------------------------------
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
            {"title": "Utilidad Neta", "value": e.utilidad_neta, "badge": f"Margen: {e.margen_utilidad_neta}%", "badge_color": "secondary"},
            {"title": "Punto de Equilibrio", "value": e.punto_equilibrio, "badge": f"Liquidez:{e.ratio_cobertura}%", "badge_color": "warning"},
            {"title": "Dividendos", "value": e.dividendos_accionistas, "badge": f"Rentabilidad: {e.rentabilidad}%", "badge_color": "success"},
        ]


        header_stats = [
        {
        "title": "Total Ingresos",
        "value": e.total_ingresos,
        "badge": "Ingresos",
        "badge_color": "primary",
         },
         {
        "title": "Total Egresos",
        "value": e.total_egresos,
        "badge": "Egresos",
        "badge_color": "warning",
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
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        x_vals = np.array(ingresos)
        y_vals = np.array(egresos)
        ax2.scatter(x_vals, y_vals, color="#e82b0c", alpha=0.75, s=60)
        if len(x_vals) > 1 and np.std(x_vals) > 0:
            m, b = np.polyfit(x_vals, y_vals, 1)
            ax2.plot(x_vals, m*x_vals+b, "-", color="#e82b0c", linewidth=3)
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
                colors=plt.cm.Blues(np.linspace(0.4, 0.8, len(ingresos_labels)))
            )
           

        if egresos_values:
            ax4.pie(
                egresos_values,
                labels=egresos_labels,
                autopct="%1.1f%%",
                startangle=90,
                colors=plt.cm.Oranges(np.linspace(0.4, 0.8, len(egresos_labels)))
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
    )

    # ----------------------------------
    # Listado
    # ----------------------------------
    list_display = (
        "fecha_inicio",
        "fecha_fin",
        "total_ingresos",
        "total_egresos",
        "utilidad_bruta",
        "utilidad_neta",
        "margen_utilidad_neta",
        "rentabilidad",
        "ratio_cobertura",
        "porcentaje_ventas"
    )

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
    )

    unfold_fieldsets = True
