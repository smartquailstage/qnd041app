from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib import admin
from .models import SPDP_ActaDelegado, Regulacion


#SCVS_Estatutos, SRI_RUC, MT_Contratos, IESS_Aportes

from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from unfold.components import BaseComponent, register_component


from .models import Regulacion

@admin.register(Regulacion)
class RegulacionAdmin(ModelAdmin):
    # Campos a mostrar en la lista de registros
    list_display = (
        "nombre_registro",
        "fecha_creacion",
        "vigente",
        "nombre_SCVS",
        "nombre_SPDP",
        "nombre_SRI",
        "nombre_MIN_TRABAJO",
        "nombre_IESS",
    )

    # Filtros en la barra lateral
    list_filter = ("vigente", "fecha_creacion")

    # Campos por los que se puede buscar
    search_fields = ("nombre_registro", "nombre_SCVS", "nombre_SPDP", "nombre_SRI", "nombre_MIN_TRABAJO", "nombre_IESS")

    # Campos de solo lectura
    readonly_fields = ("fecha_creacion",)

    # Orden por defecto
    ordering = ("-fecha_creacion",)

    

@register_component
class BalanceGeneralComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Balance General"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        i = self.instance  # SCVSFinancialReport

        headers = ["Cuenta", "Monto"]

        rows = [
            ["Efectivo y equivalentes", i.cash_and_equivalents],
            ["Inversiones a corto plazo", i.short_term_investments],
            ["Cuentas por cobrar", i.accounts_receivable],
            ["Inventarios", i.inventories],
            ["Otros activos corrientes", i.other_current_assets],
            ["Propiedad, planta y equipo", i.property_plant_equipment],
            ["Depreciación acumulada", i.accumulated_depreciation],
            ["Activos intangibles", i.intangible_assets],
            ["Otros activos no corrientes", i.other_non_current_assets],
            ["Cuentas por pagar", i.accounts_payable],
            ["Préstamos a corto plazo", i.short_term_loans],
            ["Obligaciones tributarias", i.tax_payables],
            ["Obligaciones laborales", i.labor_obligations],
            ["Otros pasivos corrientes", i.other_current_liabilities],
            ["Préstamos a largo plazo", i.long_term_loans],
            ["Provisiones", i.provisions],
            ["Otros pasivos no corrientes", i.other_non_current_liabilities],
            ["Capital social", i.share_capital],
            ["Reserva legal", i.legal_reserve],
            ["Resultados acumulados", i.retained_earnings],
            ["Resultado neto del ejercicio", i.net_income],
        ]

        context.update({
            "title": self.name,
            "table": {"headers": headers, "rows": rows},
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class EstadoResultadosComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Estado de Resultados"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        i = self.instance

        headers = ["Cuenta", "Monto"]

        rows = [
            ["Ingresos operativos", i.operating_revenue],
            ["Costo de ventas", i.cost_of_sales],
            ["Utilidad bruta", i.gross_profit],
            ["Gastos administrativos", i.administrative_expenses],
            ["Gastos de ventas", i.selling_expenses],
            ["Gastos financieros", i.financial_expenses],
            ["Otros ingresos", i.other_income],
            ["Otros gastos", i.other_expenses],
            ["Impuesto a la renta", i.income_tax],
        ]

        context.update({
            "title": self.name,
            "table": {"headers": headers, "rows": rows},
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class FlujoEfectivoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Flujo de Efectivo"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        i = self.instance

        headers = ["Actividad", "Monto"]

        rows = [
            ["Actividades de operación", i.cashflow_operating],
            ["Actividades de inversión", i.cashflow_investing],
            ["Actividades de financiamiento", i.cashflow_financing],
            ["Flujo neto de efectivo", i.net_cash_flow],
        ]

        context.update({
            "title": self.name,
            "table": {"headers": headers, "rows": rows},
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


from django.template.loader import render_to_string


@register_component
class DatosGeneralesComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Datos Generales de la Compañía"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance  # SCVSFinancialReport

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        i = self.instance

        headers = ["Campo", "Detalle"]

        rows = [
            ["RUC", i.ruc],
            ["Nombre de la compañía", i.company_name],
            ["Tipo de sociedad", i.get_company_type_display() if i.company_type else ""],
            ["Año fiscal", i.fiscal_year],
            ["Actividad económica (CIIU)", i.economic_activity],
            ["Moneda del reporte", i.currency],
        ]

        context.update({
            "title": self.name,
            "table": {"headers": headers, "rows": rows},
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


# components.py
from django.template.loader import render_to_string


@register_component
class CambiosPatrimonioComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Cambios en el Patrimonio"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        i = self.instance

        headers = ["Cuenta", "Monto"]

        rows = [
            ["Saldo inicial del patrimonio", i.equity_opening_balance],
            ["Incrementos en el patrimonio", i.equity_increases],
            ["Disminuciones del patrimonio", i.equity_decreases],
            ["Saldo final del patrimonio", i.equity_closing_balance],
        ]

        context.update({
            "title": self.name,
            "table": {"headers": headers, "rows": rows},
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class AnexosSCVSComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Anexos SCVS"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        i = self.instance

        headers = ["Cuenta", "Detalle"]

        rows = [
            ["Cuentas por cobrar relacionadas", i.accounts_receivable_related],
            ["Cuentas por pagar relacionadas", i.accounts_payable_related],
            ["Costo de activos fijos", i.fixed_assets_cost],
            ["Depreciación de activos fijos", i.fixed_assets_depreciation],
            ["Obligaciones financieras totales", i.financial_obligations_total],
            ["Participación de empleados", i.employee_profit_sharing],
        ]

        context.update({
            "title": self.name,
            "table": {"headers": headers, "rows": rows},
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


from django.utils.safestring import mark_safe
from django.urls import reverse

# -----------------------------
# Enlace TXT: Datos Generales
# -----------------------------
def SCVS_DatosGenerales(obj):
    url_txt = reverse('smartbusinesslaw:txt_datos_generales', args=[obj.id])
    url_pdf = reverse('smartbusinesslaw:pdf_datos_generales', args=[obj.id])
    return mark_safe(
        f'<a href="{url_txt}" target="_blank"><span class="material-symbols-outlined">download</span> TXT</a> | '
        f'<a href="{url_pdf}" target="_blank"><span class="material-symbols-outlined">picture_as_pdf</span> PDF</a>'
    )
SCVS_DatosGenerales.short_description = "Datos Generales"

# -----------------------------
# Enlace TXT: Balance General
# -----------------------------
def SCVS_BalanceGeneral(obj):
    url_txt = reverse('smartbusinesslaw:txt_balance_general', args=[obj.id])
    url_pdf = reverse('smartbusinesslaw:pdf_estado_resultados', args=[obj.id])
    return mark_safe(
        f'<a href="{url_txt}" target="_blank"><span class="material-symbols-outlined">download</span> TXT</a> | '
        f'<a href="{url_pdf}" target="_blank"><span class="material-symbols-outlined">picture_as_pdf</span> PDF</a>'
    )
SCVS_BalanceGeneral.short_description = "Balance General"

# -----------------------------
# Enlace TXT: Estado de Resultados
# -----------------------------
def SCVS_EstadoResultados(obj):
    url_txt = reverse('smartbusinesslaw:txt_estado_resultados', args=[obj.id])
    url_pdf = reverse('smartbusinesslaw:pdf_estado_resultados', args=[obj.id])
    return mark_safe(
        f'<a href="{url_txt}" target="_blank"><span class="material-symbols-outlined">download</span> TXT</a> | '
        f'<a href="{url_pdf}" target="_blank"><span class="material-symbols-outlined">picture_as_pdf</span> PDF</a>'
    )
SCVS_EstadoResultados.short_description = "Estado Resultados"

# -----------------------------
# Enlace TXT: Cambios en el Patrimonio
# -----------------------------
def SCVS_CambiosPatrimonio(obj):
    url_txt = reverse('smartbusinesslaw:txt_cambios_patrimonio', args=[obj.id])
    url_pdf = reverse('smartbusinesslaw:pdf_cambios_patrimonio', args=[obj.id])
    return mark_safe(
        f'<a href="{url_txt}" target="_blank"><span class="material-symbols-outlined">download</span> TXT</a> | '
        f'<a href="{url_pdf}" target="_blank"><span class="material-symbols-outlined">picture_as_pdf</span> PDF</a>'
    )
SCVS_CambiosPatrimonio.short_description = "Cambios Patrimonio"

def SCVS_FlujoAnexos(obj):
    url_txt = reverse('smartbusinesslaw:txt_flujo_anexos', args=[obj.id])
    url_pdf = reverse('smartbusinesslaw:pdf_anexos', args=[obj.id])
    return mark_safe(
        f'<a href="{url_txt}" target="_blank"><span class="material-symbols-outlined">download</span> TXT</a> | '
        f'<a href="{url_pdf}" target="_blank"><span class="material-symbols-outlined">picture_as_pdf</span> PDF</a>'
    )
SCVS_FlujoAnexos.short_description = "Flujo/Anexos"



@admin.register(SCVSFinancialReport)
class SCVSFinancialReportAdmin(ModelAdmin):
    # ---------------------------
    # Componentes renderizados
    # ---------------------------
    list_sections = [
        DatosGeneralesComponent,
        BalanceGeneralComponent,
        EstadoResultadosComponent,
        CambiosPatrimonioComponent,
        FlujoEfectivoComponent,
        AnexosSCVSComponent,
    ]

    # ---------------------------
    # Fieldsets clásicos (solo con campos del modelo)
    # ---------------------------
    fieldsets = (
        ('Datos Generales', {
            'fields': ('ruc', 'company_name', 'company_type', 'fiscal_year', 'economic_activity', 'currency'),
            'classes': ('unfold', 'tab-datos-generales'),
        }),
        ('Balance General', {
            'fields': (
                'cash_and_equivalents', 'short_term_investments', 'accounts_receivable', 'inventories',
                'other_current_assets', 'property_plant_equipment', 'accumulated_depreciation',
                'intangible_assets', 'other_non_current_assets', 'accounts_payable', 'short_term_loans',
                'tax_payables', 'labor_obligations', 'other_current_liabilities', 'long_term_loans',
                'provisions', 'other_non_current_liabilities', 'share_capital', 'legal_reserve',
                'retained_earnings', 'net_income'
            ),
            'classes': ('unfold', 'tab-balance-general'),
        }),
        ('Estado de Resultados', {
            'fields': (
                'operating_revenue', 'cost_of_sales', 'gross_profit', 'administrative_expenses',
                'selling_expenses', 'financial_expenses', 'other_income', 'other_expenses', 'income_tax'
            ),
            'classes': ('unfold', 'tab-estado-resultados'),
        }),
        ('Cambios en el Patrimonio', {
            'fields': ('equity_opening_balance', 'equity_increases', 'equity_decreases', 'equity_closing_balance'),
            'classes': ('unfold', 'tab-cambios-patrimonio'),
        }),
        ('Flujo de Efectivo', {
            'fields': ('cashflow_operating', 'cashflow_investing', 'cashflow_financing', 'net_cash_flow'),
            'classes': ('unfold', 'tab-flujo-efectivo'),
        }),
        ('Anexos SCVS', {
            'fields': (
                'accounts_receivable_related', 'accounts_payable_related', 'fixed_assets_cost',
                'fixed_assets_depreciation', 'financial_obligations_total', 'employee_profit_sharing'
            ),
            'classes': ('unfold', 'tab-anexos-scvs'),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('unfold', 'tab-metadata'),
        }),
    )

    # ---------------------------
    # Listado principal
    # ---------------------------
    list_display = ('fiscal_year',
    SCVS_DatosGenerales,
    SCVS_BalanceGeneral,
    SCVS_EstadoResultados,
    SCVS_CambiosPatrimonio,
    SCVS_FlujoAnexos,
    )

    list_filter = ('fiscal_year', 'company_type')

    search_fields = ('company_name', 'ruc')

    readonly_fields = ('created_at', 'updated_at')

    unfold_fieldsets = True

# -------------------------------
# SPDP_ActaDelegado PDFs
# -------------------------------

def delegado_pdf_link(obj):
    """PDF general DPD"""
    url = reverse('smartbusinesslaw:admin_delegado_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}" target="_blank"><span class="material-symbols-outlined">download</span> Descargar</a>')
delegado_pdf_link.short_description = "CERTIFICADO (DPD)"

def rat_pdf_link(obj):
    """PDF del Registro de Actividades de Tratamiento"""
    url = reverse('smartbusinesslaw:admin_rat_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}" target="_blank"><span class="material-symbols-outlined">download</span>Descarga</a>')
rat_pdf_link.short_description = "CERTIFICADO (RAT)"

def incidente_pdf_link(obj):
    """PDF de Incidentes y Mitigaciones"""
    url = reverse('smartbusinesslaw:admin_incidente_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}" target="_blank"><span class="material-symbols-outlined">download</span>Descarga</a>')
incidente_pdf_link.short_description = "CERTIFICADO (EIPD/DPIA)"



from django.utils import timezone
from django.urls import reverse
from django.utils.safestring import mark_safe


def VENCIMIENTO(obj):
    """
    PDF de Incidentes y Mitigaciones
    Muestra tiempo restante antes de expiración (días, horas, minutos)
    """
    url = reverse('smartbusinesslaw:admin_incidente_pdf', args=[obj.id])

    # ⏳ Cálculo del tiempo restante
    if obj.fecha_expiracion:
        now = timezone.now()
        delta = obj.fecha_expiracion - now

        if delta.total_seconds() > 0:
            dias = delta.days
            horas, remainder = divmod(delta.seconds, 3600)
            minutos = remainder // 60

            tiempo_restante = (
                f"{dias}d {horas}h {minutos}m"
            )
            estado = f"<small style='color:#2e7d32;'>⏳ {tiempo_restante}</small>"
        else:
            estado = "<small style='color:#c62828;'>⛔ EXPIRADO</small>"
    else:
        estado = "<small style='color:#757575;'>— sin fecha —</small>"

    return mark_safe(
        f"""
        {estado}
        """
    )


incidente_pdf_link.short_description = "CERTIFICADO EIPD / DPIA"





# -------------------------------
# Regulacion PDF
# -------------------------------

def regulacion_pdf_link(obj):
    """PDF de la regulación / base legal"""
    url = reverse('smartbusinesslaw:admin_regulacion_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}" target="_blank">Ver PDF</a>')
regulacion_pdf_link.short_description = "PDF"






from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from unfold.components import BaseComponent, register_component


@register_component
class ActaDelegadoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Delegado de Protección de Datos (DPD)"
    

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = self.instance  # instancia SPDP_ActaDelegado

        headers = [
            "Campo",
            "Valor",
        ]

        rows = [
            ["Delegado (DPD)", a.nombre_delegado],
            ["Identificación", a.identificacion_delegado],
            ["Correo electrónico", a.correo_delegado],
            ["Teléfono", a.telefono_delegado],
            ["Fecha de nombramiento", a.fecha_nombramiento],
            ["Acto de designación", a.acto_designacion],
            ["Tipo de vinculación", a.get_tipo_vinculacion_display() if a.tipo_vinculacion else ""],
            ["Declaración de independencia", "Sí" if a.declaracion_independencia else "No"],
            ["Declaración de confidencialidad", "Sí" if a.declaracion_confidencialidad else "No"],
        ]

        context.update({
            "title": "Información del Delegado de Protección de Datos (DPD)",
            "table": {
                "headers": headers,
                "rows": rows,
            }
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())




@register_component
class ActaIncidenteComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Registro de Incidencias de Seguridad"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        i = self.instance  # SPDP_ActaDelegado

        headers = [
            "Campo",
            "Detalle",
        ]

        rows = [
            ["Código del incidente", i.incidente_identificacion],
            ["Fecha de detección", i.incidente_fecha_deteccion],
            ["Tipo de incidente", i.incidente_tipo],
            ["Estado", i.get_incidente_estado_display() if i.incidente_estado else ""],
            ["Nivel de riesgo", i.incidente_riesgo],
            ["Datos afectados", i.incidente_datos_afectados],
            ["Titulares afectados", i.incidente_titulares_afectados],
            ["Notificado a la SPDP", "Sí" if i.incidente_notificado_spdp else "No"],
            ["Fecha de notificación", i.incidente_fecha_notificacion],
            ["Medidas de mitigación", i.incidente_medidas_mitigacion],
            ["Medidas correctivas", i.incidente_medidas_correctivas],
            ["Observaciones", i.observaciones],
        ]

        context.update({
            "title": "Registro de Incidencias de Seguridad",
            "table": {
                "headers": headers,
                "rows": rows,
            }
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())





# ===========================
# SCVS_Estatutos Admin
# ===========================
@admin.register(SCVS_Estatutos)
class SCVS_EstatutosAdmin(ModelAdmin):
    fieldsets = (
        ('Información General', {
            'fields': ('regulacion', 'nombre_empresa', 'fecha_aprobacion', 'notario'),
            'classes': ('unfold', 'tab-general'),
        }),
        ('Archivo', {
            'fields': ('archivo',),
            'classes': ('unfold', 'tab-archivo'),
        }),
    )
    list_display = ('nombre_empresa', 'fecha_aprobacion', 'notario', 'regulacion')
    list_filter = ('fecha_aprobacion', 'regulacion')
    unfold_fieldsets = True


def SCVS_ActaJunta(obj):
    url_pdf = reverse('smartbusinesslaw:pdf_acta_junta', args=[obj.id])
    return mark_safe(
        f'<a href="{url_pdf}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>Descargar</a>'
    )
SCVS_ActaJunta.short_description = "Acta Junta"



def SCVS_NominaSocios(obj):
    url_pdf = reverse('smartbusinesslaw:pdf_nomina_socios', args=[obj.id])
    return mark_safe(
        f'<a href="{url_pdf}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>Descargar</a>'
    )
SCVS_NominaSocios.short_description = "Nómina Socios"



def SCVS_NominaAdministradores(obj):
    url_pdf = reverse('smartbusinesslaw:pdf_nomina_administradores', args=[obj.id])
    return mark_safe(
        f'<a href="{url_pdf}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>Descargar</a>'
    )
SCVS_NominaAdministradores.short_description = "Nómina Administradores"


def SCVS_InformeGerente(obj):
    url_pdf = reverse('smartbusinesslaw:pdf_informe_gerente', args=[obj.id])
    return mark_safe(
        f'<a href="{url_pdf}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>Descargar</a>'
    )
SCVS_InformeGerente.short_description = "Informe Gerente"


def SCVS_BalanceGeneral(obj):
    url_pdf = reverse('smartbusinesslaw:pdf_balance', args=[obj.id])
    return mark_safe(
        f'<a href="{url_pdf}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>Descargar</a>'
    )
SCVS_BalanceGeneral.short_description = "Balance General"


def SCVS_EstadoResultados(obj):
    url_pdf = reverse('smartbusinesslaw:pdf_estado_resultados', args=[obj.id])
    return mark_safe(
        f'<a href="{url_pdf}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>Descargar</a>'
    )
SCVS_EstadoResultados.short_description = "Estado Resultados"



# ===========================
# SPDP_ActaDelegado Admin
# ===========================
@admin.register(SPDP_ActaDelegado)
class SPDP_ActaDelegadoAdmin(ModelAdmin):
    list_sections = [
    ActaDelegadoComponent,ActaIncidenteComponent,
    ]




    fieldsets = (

        # ---------------------------------------------------
        # 1. DOCUMENTO DEL DELEGADO DE PROTECCIÓN DE DATOS
        # ---------------------------------------------------
        ('Documento del Delegado de Protección de Datos (DPD)', {
            'fields': (
                'regulacion',
                'nombre_delegado',
                'identificacion_delegado',
                'correo_delegado',
                'telefono_delegado',
                'fecha_nombramiento',
                'acto_designacion',
                'tipo_vinculacion',
                'funciones_delegado',
                'declaracion_independencia',
                'declaracion_confidencialidad',
       
            ),
            'classes': ('unfold', 'tab-dpd'),
        }),

        # ---------------------------------------------------
        # 2. REGISTRO DE ACTIVIDADES DE TRATAMIENTO (RAT)
        # ---------------------------------------------------
        ('Registro de Actividades de Tratamiento (RAT)', {
            'fields': (
                'rat_nombre_tratamiento',
                'rat_finalidad',
                'rat_base_legal',
                'rat_categoria_datos',
                'rat_categoria_titulares',
                'rat_categoria_destinatarios',
                'rat_responsable_tratamiento',
                'rat_titular_datos',
                'rat_plazo_conservacion',
                'rat_transferencias_internacionales',
                'rat_pais_transferencia',
                'rat_medidas_tecnicas',
                'rat_medidas_organizativas',
            ),
            'classes': ('unfold', 'tab-rat'),
        }),

        # ---------------------------------------------------
        # 3. REGISTRO DE INCIDENTES Y MITIGACIONES
        # ---------------------------------------------------
        ('Registro de Incidentes de Seguridad y Mitigación', {
            'fields': (
                'incidente_identificacion',
                'incidente_fecha_deteccion',
                'incidente_tipo',
                'incidente_descripcion',
                'incidente_datos_afectados',
                'incidente_titulares_afectados',
                'incidente_riesgo',
                'incidente_notificado_spdp',
                'incidente_fecha_notificacion',
                'incidente_medidas_mitigacion',
                'incidente_medidas_correctivas',
                'incidente_estado',
                'archivo_incidente',
            ),
            'classes': ('unfold', 'tab-incidentes'),
        }),

        # ---------------------------------------------------
        # 4. CONTROL Y OBSERVACIONES
        # ---------------------------------------------------
        ('Control y Observaciones', {
            'fields': (
                'observaciones',
                'fecha_creacion',
                'fecha_actualizacion',
            ),
            'classes': ('unfold', 'tab-control'),
        }),
    )

    # -------------------------
    # Listados
    # -------------------------
    list_display = (
        'nombre_delegado',
        'rat_titular_datos',
        VENCIMIENTO,
        delegado_pdf_link,       # Enlace PDF DPD
        rat_pdf_link,            # Enlace PDF RAT
        incidente_pdf_link, 
        'legalizado_spd',
    )

    list_editable = ['legalizado_spd']

    list_filter = (
        'fecha_nombramiento',
        'rat_transferencias_internacionales',
        'incidente_estado',
        'incidente_notificado_spdp',
        'regulacion',
    )

    search_fields = (
        'nombre_delegado',
        'rat_nombre_tratamiento',
        'incidente_identificacion',
    )

    readonly_fields = (
        'fecha_creacion',
        'fecha_actualizacion',
    )

    unfold_fieldsets = True


# ===========================
# SRI_RUC Admin
# ===========================
@admin.register(SRI_RUC)
class SRI_RUCAdmin(ModelAdmin):
    fieldsets = (
        ('Información RUC', {
            'fields': ('regulacion', 'ruc', 'fecha_emision'),
            'classes': ('unfold', 'tab-general'),
        }),
        ('Archivo', {
            'fields': ('archivo',),
            'classes': ('unfold', 'tab-archivo'),
        }),
    )
    list_display = ('ruc', 'fecha_emision', 'regulacion')
    list_filter = ('fecha_emision', 'regulacion')
    unfold_fieldsets = True

# ===========================
# MT_Contratos Admin
# ===========================
@admin.register(MT_Contratos)
class MT_ContratosAdmin(ModelAdmin):
    fieldsets = (
        ('Información del Contrato', {
            'fields': ('regulacion', 'empleado', 'fecha_inicio', 'fecha_fin', 'tipo_contrato'),
            'classes': ('unfold', 'tab-general'),
        }),
        ('Archivo', {
            'fields': ('archivo',),
            'classes': ('unfold', 'tab-archivo'),
        }),
    )
    list_display = ('empleado', 'tipo_contrato', 'fecha_inicio', 'fecha_fin', 'regulacion')
    list_filter = ('tipo_contrato', 'fecha_inicio', 'regulacion')
    unfold_fieldsets = True

# ===========================
# IESS_Aportes Admin
# ===========================
@admin.register(IESS_Aportes)
class IESS_AportesAdmin(ModelAdmin):
    fieldsets = (
        ('Información Aporte', {
            'fields': ('regulacion', 'empleado', 'ejercicio_fiscal', 'mes', 'monto', 'fecha_pago'),
            'classes': ('unfold', 'tab-general'),
        }),
        ('Archivo', {
            'fields': ('archivo',),
            'classes': ('unfold', 'tab-archivo'),
        }),
    )
    list_display = ('empleado', 'periodo', 'monto', 'fecha_pago', 'regulacion')
    list_filter = ('periodo', 'regulacion')
    unfold_fieldsets = True



from .models import SCVS_ActasAsamblea


@register_component
class ActaJuntaGeneralComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Acta de Junta General"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = self.instance

        rows = [
            ["Tipo de junta", a.tipo_junta],
            ["Fecha de asamblea", a.fecha_asamblea],
            ["Hora de inicio", a.hora_inicio],
            ["Hora de cierre", a.hora_cierre],
            ["Lugar", a.lugar_asamblea],
            ["Ejercicio fiscal", a.ejercicio_fiscal],
            ["Forma de convocatoria", a.forma_convocatoria],
            ["Fecha de convocatoria", a.fecha_convocatoria],
            ["Quórum válido", "Sí" if a.quorum_valido else "No"],
            ["Capital presente", a.capital_presente],
            ["Porcentaje asistencia", a.porcentaje_asistencia],
            ["Presidente", a.presidente_junta],
            ["Secretario", a.secretario_junta],
            ["Orden del día", a.orden_dia],
            ["Resoluciones", a.resoluciones],
        ]

        context.update({
            "title": "Acta de Junta General",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class NominaSociosComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Nómina de Socios / Accionistas"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = self.instance

        rows = [
            ["Año fiscal", a.socios_anio_fiscal],
            ["Fecha de corte", a.socios_fecha_corte],
            ["Tipo de compañía", a.socios_tipo_compania],
            ["Detalle de socios", a.socios_detalle],
            ["Total socios", a.socios_total_numero],
            ["Capital suscrito total", a.socios_capital_suscrito_total],
            ["Capital pagado total", a.socios_capital_pagado_total],
            ["Representante legal", a.socios_representante_legal],
            ["Contador", a.socios_contador],
            ["Fecha certificación", a.socios_fecha_certificacion],
        ]

        context.update({
            "title": "Nómina de Socios / Accionistas (SCVS 3.1.3)",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())



@register_component
class NominaAdministradoresComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Nómina de Administradores"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = self.instance

        rows = [
            ["Año fiscal", a.admins_anio_fiscal],
            ["Fecha vigencia", a.admins_fecha_vigencia],
            ["Detalle administradores", a.admins_detalle],
            ["Representante legal vigente", "Sí" if a.admins_representante_legal_vigente else "No"],
            ["Observaciones", a.admins_observaciones],
            ["Representante legal", a.admins_representante_legal],
            ["Secretario", a.admins_secretario],
            ["Fecha certificación", a.admins_fecha_certificacion],
        ]

        context.update({
            "title": "Nómina de Administradores (SCVS 3.1.8)",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())




@register_component
class InformeGerenteComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Informe de Gerente General"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = self.instance

        rows = [
            ["Año fiscal", a.gerente_anio_fiscal],
            ["Gerente general", a.gerente_nombre],
            ["Cargo", a.gerente_cargo],
            ["Periodo informado", a.gerente_periodo_informado],
            ["Introducción", a.gerente_introduccion],
            ["Situación financiera", a.gerente_situacion_financiera],
            ["Desempeño operativo", a.gerente_desempeno_operativo],
            ["Eventos relevantes", a.gerente_eventos_relevantes],
            ["Riesgos", a.gerente_riesgos],
            ["Cumplimiento legal", a.gerente_cumplimiento_legal],
            ["Proyecciones", a.gerente_proyecciones],
            ["Conclusión", a.gerente_conclusion],
            ["Declaración de responsabilidad", a.gerente_declaracion_responsabilidad],
            ["Gerente firmante", a.gerente_firma],
            ["Representante legal", a.gerente_representante_legal],
            ["Abogado patrocinador", a.gerente_abogado],
            ["Fecha emisión", a.gerente_fecha_emision],
        ]

        context.update({
            "title": "Informe de Gerente (SCVS 3.1.5)",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class SCVSChecklistComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Checklist Documental SCVS"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = self.instance

        rows = [
            ["Acta de Junta", "✔️" if a.fecha_asamblea else "❌"],
            ["Nómina de Socios", "✔️" if a.socios_detalle else "❌"],
            ["Nómina de Administradores", "✔️" if a.admins_detalle else "❌"],
            ["Informe de Gerente", "✔️" if a.gerente_introduccion else "❌"],
            ["Archivo PDF cargado", "✔️" if a.archivo else "❌"],
        ]

        context.update({
            "title": "Checklist SCVS",
            "table": {"headers": ["Documento", "Estado"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import SCVS_ActasAsamblea

# ===========================
# SCVS_ActasAsamblea Admin
# ===========================
@admin.register(SCVS_ActasAsamblea)
class SCVS_ActasAsambleaAdmin(ModelAdmin):

    # ----------------------------------
    # Componentes visuales (cards)
    # ----------------------------------
    list_sections = [
        SCVSChecklistComponent,
        ActaJuntaGeneralComponent,
        NominaSociosComponent,
        NominaAdministradoresComponent,
        InformeGerenteComponent,
    ]

    fieldsets = (

        # ---------------------------------------------------
        # 1. ACTA DE JUNTA GENERAL (SCVS 3.1.N)
        # ---------------------------------------------------
        ('Acta de Junta General de Socios / Accionistas', {
            'fields': (
                'regulacion',
                'tipo_junta',
                'fecha_asamblea',
                'hora_inicio',
                'hora_cierre',
                'lugar_asamblea',
                'ejercicio_fiscal',
                'forma_convocatoria',
                'fecha_convocatoria',
                'quorum_valido',
                'capital_presente',
                'porcentaje_asistencia',
                'presidente_junta',
                'secretario_junta',
                'orden_dia',
                'resoluciones',
            ),
            'classes': ('unfold', 'tab-acta'),
        }),

        # ---------------------------------------------------
        # 2. NÓMINA DE SOCIOS / ACCIONISTAS (SCVS 3.1.3)
        # ---------------------------------------------------
        ('Nómina de Socios / Accionistas', {
            'fields': (
                'socios_anio_fiscal',
                'socios_fecha_corte',
                'socios_tipo_compania',
                'socios_detalle',
                'socios_total_numero',
                'socios_capital_suscrito_total',
                'socios_capital_pagado_total',
                'socios_representante_legal',
                'socios_contador',
                'socios_fecha_certificacion',
            ),
            'classes': ('unfold', 'tab-socios'),
        }),

        # ---------------------------------------------------
        # 3. NÓMINA DE ADMINISTRADORES (SCVS 3.1.8)
        # ---------------------------------------------------
        ('Nómina de Administradores', {
            'fields': (
                'admins_anio_fiscal',
                'admins_fecha_vigencia',
                'admins_detalle',
                'admins_representante_legal_vigente',
                'admins_observaciones',
                'admins_representante_legal',
                'admins_secretario',
                'admins_fecha_certificacion',
            ),
            'classes': ('unfold', 'tab-administradores'),
        }),

        # ---------------------------------------------------
        # 4. INFORME DE GERENTE GENERAL (SCVS 3.1.5)
        # ---------------------------------------------------
        ('Informe de Gerente General', {
            'fields': (
                'gerente_anio_fiscal',
                'gerente_nombre',
                'gerente_cargo',
                'gerente_periodo_informado',
                'gerente_introduccion',
                'gerente_situacion_financiera',
                'gerente_desempeno_operativo',
                'gerente_eventos_relevantes',
                'gerente_riesgos',
                'gerente_cumplimiento_legal',
                'gerente_proyecciones',
                'gerente_conclusion',
                'gerente_declaracion_responsabilidad',
                'gerente_firma',
                'gerente_representante_legal',
                'gerente_abogado',
                'gerente_fecha_emision',
            ),
            'classes': ('unfold', 'tab-gerente'),
        }),

        # ---------------------------------------------------
        # 5. ARCHIVOS Y CONTROL
        # ---------------------------------------------------
        ('Control y Documentos', {
            'fields': (
                'archivo',
            ),
            'classes': ('unfold', 'tab-control'),
        }),
    )

    # -------------------------
    # Listado principal
    # -------------------------
    list_display = (
    'ejercicio_fiscal',
    # --- Documentos SCVS (PDF) ---
    SCVS_ActaJunta,                # 3.1.N Acta de Junta General
    SCVS_NominaSocios,             # 3.1.3 Nómina de Socios / Accionistas
    SCVS_NominaAdministradores,    # 3.1.8 Nómina de Administradores
    SCVS_InformeGerente,           # 3.1.5 Informe de Gerente
    SCVS_BalanceGeneral,           # 3.1.1 Balance General
    )


    list_filter = (
        'ejercicio_fiscal',
        'tipo_junta',
        'socios_tipo_compania',
        'admins_representante_legal_vigente',
        'regulacion',
    )

    search_fields = (
        'presidente_junta',
        'secretario_junta',
        'gerente_nombre',
        'socios_detalle',
        'admins_detalle',
    )


    unfold_fieldsets = True


from django.utils.safestring import mark_safe
from django.urls import reverse

# ==================================================
# ATS
# ==================================================


def mes(obj):
    meses = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre",
    }
    return meses.get(obj.mes, "—")
mes.short_description = "Mes"

def ZIP_ATS(obj):
    url_zip = reverse('smartbusinesslaw:zip_ats', args=[obj.ruc, obj.ejercicio_fiscal, obj.mes])
    display_value = f"{obj.ventas_total}"  # ejemplo: mostrar total de ventas como valor del ATS
    return mark_safe(
        f'<a href="{url_zip}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>Descargar</a>'
    )
ZIP_ATS.short_description = "ATS"

# ==================================================
# RDEP
# ==================================================
def ZIP_RDEP(obj):
    url_zip = reverse('smartbusinesslaw:zip_rdep', args=[obj.ruc, obj.ejercicio_fiscal, obj.mes])
    display_value = f"{obj.cantidad_empleados}" if obj.tiene_empleados else "0"
    return mark_safe(
        f'<a href="{url_zip}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>Descargar</a>  </a>'
    )
ZIP_RDEP.short_description = "RDEP"

# ==================================================
# Dividendos
# ==================================================
def ZIP_Dividendos(obj):
    url_zip = reverse('smartbusinesslaw:zip_dividendos', args=[obj.ruc, obj.ejercicio_fiscal, obj.mes])
    display_value = f"{obj.dividendo_pagado or 0}"  # mostrar monto de dividendos
    return mark_safe(
        f'<a href="{url_zip}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>Descargar</a>'
    )
ZIP_Dividendos.short_description = "ADI"

# ==================================================
# Partes Relacionadas
# ==================================================
def ZIP_PartesRelacionadas(obj):
    url_zip = reverse('smartbusinesslaw:zip_partes_relacionadas', args=[obj.ruc, obj.ejercicio_fiscal, obj.mes])
    display_value = f"{obj.monto_operacion_parte_relacionada or 0}"  # monto de operaciones
    return mark_safe(
        f'<a href="{url_zip}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>Descargar</a>'
    )
ZIP_PartesRelacionadas.short_description = "OPR"

# ==================================================
# Conciliación Tributaria
# ==================================================
def ZIP_Conciliacion(obj):
    url_zip = reverse('smartbusinesslaw:zip_conciliacion', args=[obj.ruc, obj.ejercicio_fiscal, obj.mes])
    display_value = f"{obj.utilidad_contable or 0}"  # mostrar utilidad contable
    return mark_safe(
        f'<a href="{url_zip}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>Descargar</a>'
    )
ZIP_Conciliacion.short_description = "Conciliación Tributaria"


def ZIP_BENEFICIARIOS(obj):
    url_zip = reverse('smartbusinesslaw:zip_beneficiarios_finales', args=[obj.ruc, obj.ejercicio_fiscal, obj.mes])
    display_value = f"{obj.dividendo_pagado or 0}"  # mostrar dividendo pagado como valor principal
    return mark_safe(
        f'<a href="{url_zip}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>Descargar</a>'
    )
ZIP_BENEFICIARIOS.short_description = "REBEFICS"



from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from django.template.loader import render_to_string

from .models import SRI_AnexosTributarios

# ===========================
# COMPONENTES VISUALES (CARDS)
# ===========================

@register_component
class ATSComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "ATS – Compras y Ventas"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        a = self.instance
        rows = [
            ["Tipo comprobante compra", a.compras_tipo_comprobante],
            ["ID proveedor", a.compras_id_proveedor],
            ["Razón social proveedor", a.compras_razon_social_proveedor],
            ["Fecha emisión", a.compras_fecha_emision],
            ["Base IVA 0%", a.compras_base_iva_0],
            ["Base gravada IVA", a.compras_base_iva],
            ["IVA", a.compras_monto_iva],
            ["Total compra", a.compras_total],
            ["Ventas Base IVA 0%", a.ventas_base_iva_0],
            ["Ventas Base gravada IVA", a.ventas_base_iva],
            ["IVA ventas", a.ventas_monto_iva],
            ["Total ventas", a.ventas_total],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "ATS – Compras y Ventas",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())

@register_component
class BeneficiariosComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Beneficiarios Finales"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        a = self.instance
        rows = []

        # Solo agregar si distribuyó dividendos
        if a.distribuyo_dividendos:
            rows.append(["Tipo identificación socio", a.socio_tipo_id])
            rows.append(["Identificación socio", a.socio_identificacion])
            rows.append(["Nombre socio", a.socio_nombre])
            rows.append(["Porcentaje participación", a.socio_porcentaje_participacion])
            rows.append(["Dividendo recibido", a.dividendo_pagado])
            rows.append(["Impuesto retenido", a.impuesto_dividendo])
        else:
            rows.append(["No se distribuyeron dividendos", ""])

        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Beneficiarios Finales",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())



@register_component
class ATS_RetencionesComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "ATS – Retenciones"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        a = self.instance
        rows = [
            ["Código ret IR", a.retencion_ir_codigo],
            ["% ret IR", a.retencion_ir_porcentaje],
            ["Valor ret IR", a.retencion_ir_valor],
            ["Código ret IVA", a.retencion_iva_codigo],
            ["% ret IVA", a.retencion_iva_porcentaje],
            ["Valor ret IVA", a.retencion_iva_valor],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "ATS – Retenciones",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class RDEPComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "RDEP – Relación de Dependencia"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        a = self.instance
        rows = [
            ["Tiene empleados", a.tiene_empleados],
            ["ID empleado", a.empleado_identificacion],
            ["Nombre empleado", a.empleado_nombres],
            ["Cargo", a.empleado_cargo],
            ["Sueldo anual", a.empleado_sueldo_anual],
            ["Aporte IESS", a.empleado_aporte_iess],
            ["IR retenido", a.empleado_ir_retenido],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "RDEP – Relación de Dependencia",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class DividendosComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "ADI"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        a = self.instance
        rows = [
            ["Distribuyó dividendos", a.distribuyo_dividendos],
            ["ID socio", a.socio_identificacion],
            ["Nombre socio", a.socio_nombre],
            ["% participación", a.socio_porcentaje_participacion],
            ["Dividendo pagado", a.dividendo_pagado],
            ["Impuesto dividendos", a.impuesto_dividendo],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Dividendos",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class PartesRelacionadasComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Partes Relacionadas"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        a = self.instance
        rows = [
            ["Tiene partes relacionadas", a.tiene_partes_relacionadas],
            ["ID parte relacionada", a.parte_relacionada_identificacion],
            ["Nombre parte relacionada", a.parte_relacionada_nombre],
            ["Monto operación", a.monto_operacion_parte_relacionada],
            ["Tipo operación", a.tipo_operacion],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Partes Relacionadas",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class ConciliacionTributariaComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Conciliación Tributaria"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        a = self.instance
        rows = [
            ["Utilidad contable", a.utilidad_contable],
            ["Gastos no deducibles", a.gastos_no_deducibles],
            ["Ingresos exentos", a.ingresos_exentos],
            ["Base imponible IR", a.base_imponible],
            ["Impuesto renta causado", a.impuesto_renta_causado],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Conciliación Tributaria",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


# ===========================
# ADMIN DE SRI_AnexosTributarios
# ===========================
@admin.register(SRI_AnexosTributarios)
class SRI_AnexosTributariosAdmin(ModelAdmin):

    list_sections = [
        ATSComponent,
        ATS_RetencionesComponent,
        RDEPComponent,
        DividendosComponent,
        PartesRelacionadasComponent,
        ConciliacionTributariaComponent,
        BeneficiariosComponent,  # <-- agregado
    ]

    fieldsets = (
        ("I. Identificación contribuyente", {
            "fields": (
                "ruc", "razon_social", "ejercicio_fiscal", "mes", "obligado_contabilidad",
            ),
            "classes": ("unfold", "tab-identificacion"),
        }),
        ("II. ATS – Compras y Ventas", {
            "fields": (
                "compras_tipo_comprobante", "compras_tipo_id_proveedor", "compras_id_proveedor",
                "compras_razon_social_proveedor", "compras_fecha_emision", "compras_establecimiento",
                "compras_punto_emision", "compras_secuencial", "compras_autorizacion",
                "compras_base_no_objeto_iva", "compras_base_iva_0", "compras_base_iva",
                "compras_monto_iva", "compras_total", "ventas_tipo_id_cliente",
                "ventas_id_cliente", "ventas_razon_social_cliente", "ventas_base_iva_0",
                "ventas_base_iva", "ventas_monto_iva", "ventas_total",
            ),
            "classes": ("unfold", "tab-ats"),
        }),
        ("III. ATS – Retenciones", {
            "fields": (
                "retencion_ir_codigo", "retencion_ir_porcentaje", "retencion_ir_valor",
                "retencion_iva_codigo", "retencion_iva_porcentaje", "retencion_iva_valor",
            ),
            "classes": ("unfold", "tab-retenciones"),
        }),
        ("IV. RDEP – Relación de Dependencia", {
            "fields": (
                "tiene_empleados", "empleado_tipo_id", "empleado_identificacion",
                "empleado_nombres", "empleado_cargo", "empleado_sueldo_anual",
                "empleado_aporte_iess", "empleado_ir_retenido",
            ),
            "classes": ("unfold", "tab-rdep"),
        }),
        ("VI. Partes Relacionadas", {
            "fields": (
                "tiene_partes_relacionadas", "parte_relacionada_identificacion",
                "parte_relacionada_nombre", "monto_operacion_parte_relacionada", "tipo_operacion",
            ),
            "classes": ("unfold", "tab-partes"),
        }),
        ("VII. Conciliación Tributaria", {
            "fields": (
                "utilidad_contable", "gastos_no_deducibles", "ingresos_exentos",
                "base_imponible", "impuesto_renta_causado",
            ),
            "classes": ("unfold", "tab-conciliacion"),
        }),
        ("VIII. Beneficiarios Finales", {  # <-- nuevo tab
            "fields": (
                "distribuyo_dividendos", "socio_tipo_id", "socio_identificacion", "socio_nombre",
                "socio_porcentaje_participacion", "dividendo_pagado", "impuesto_dividendo",
            ),
            "classes": ("unfold", "tab-beneficiarios"),
        }),
        ("IX. Firmas y responsabilidad", {
            "fields": ("representante_legal", "contador", "fecha_certificacion",),
            "classes": ("unfold", "tab-firmas"),
        }),
    )
    
    list_display = (
        "ejercicio_fiscal",
        mes,
      
        ZIP_ATS,
        ZIP_Dividendos,
        ZIP_RDEP,
        ZIP_PartesRelacionadas,
        ZIP_BENEFICIARIOS,  # <-- agregado
        ZIP_Conciliacion,
    )

    list_filter = (
        "ejercicio_fiscal", "mes", "obligado_contabilidad",
    )

    search_fields = (
        "ruc", "razon_social",
    )

    unfold_fieldsets = True


from .models import SRI_DeclaracionImpuestos

@register_component
class IdentificacionComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Identificación del Contribuyente"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        a = self.instance
        rows = [
            ["RUC", a.ruc],
            ["Razón social", a.razon_social],
            ["Régimen", a.get_regimen_display() if a.regimen else ""],
            ["Ejercicio fiscal", a.ejercicio_fiscal],
            ["Fecha declaración", a.fecha_declaracion],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Identificación del contribuyente",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(
            self.template_name,
            self.get_context_data()
        )


@register_component
class IVAComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Impuesto al Valor Agregado (IVA)"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        a = self.instance
        rows = [
            ["IVA en ventas", a.iva_ventas],
            ["IVA en compras", a.iva_compras],
            ["IVA a pagar", a.iva_a_pagar],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "IVA",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(
            self.template_name,
            self.get_context_data()
        )



@register_component
class RentaComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Impuesto a la Renta"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        a = self.instance
        rows = [
            ["Ingresos gravados", a.ingresos_gravados],
            ["Costos y gastos deducibles", a.costos_gastos_deducibles],
            ["Base imponible", a.base_imponible_renta],
            ["Impuesto causado", a.impuesto_renta_causado],
            ["Anticipos", a.anticipos_renta],
            ["Renta a pagar", a.renta_a_pagar],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Impuesto a la Renta",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(
            self.template_name,
            self.get_context_data()
        )



@register_component
class RetencionesComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Retenciones en la fuente"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        a = self.instance
        rows = [
            ["Retención IVA", a.retencion_iva],
            ["Retención Renta", a.retencion_renta],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Retenciones en la fuente",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(
            self.template_name,
            self.get_context_data()
        )



@register_component
class ICEISDComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "ICE e ISD"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        a = self.instance
        rows = [
            ["ICE causado", a.ice_causado],
            ["Pagos al exterior", a.pagos_exterior],
            ["ISD causado", a.isd_causado],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "ICE e ISD",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(
            self.template_name,
            self.get_context_data()
        )

@register_component
class PatenteComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Patente Municipal"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        a = self.instance
        rows = [
            ["Base patente", a.base_patente],
            ["Patente municipal", a.patente_municipal],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Patente Municipal",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(
            self.template_name,
            self.get_context_data()
        )


@admin.register(SRI_DeclaracionImpuestos)
class SRI_DeclaracionImpuestosAdmin(ModelAdmin):

    list_sections = [
        IdentificacionComponent,
        IVAComponent,
        RentaComponent,
        RetencionesComponent,
        ICEISDComponent,
        PatenteComponent,
    ]

    readonly_fields = (
        "iva_a_pagar",
        "base_imponible_renta",
        "renta_a_pagar",
        "isd_causado",
        "creado_en",
        "actualizado_en",      
    )

    fieldsets = (
        ("I. Identificación del contribuyente", {
            "fields": (
                "ruc", "razon_social", "regimen",
                "ejercicio_fiscal", "mes", "fecha_declaracion", "cp","archivo_auditoria", "declarado",
            ),
            "classes": ("unfold", "tab-identificacion"),
        }),
        ("II. IVA", {
            "fields": (
                "iva_ventas", "iva_compras", "iva_a_pagar",
            ),
            "classes": ("unfold", "tab-iva"),
        }),
        ("III. Impuesto a la Renta", {
            "fields": (
                "ingresos_gravados", "costos_gastos_deducibles",
                "base_imponible_renta", "impuesto_renta_causado",
                "anticipos_renta", "renta_a_pagar",
            ),
            "classes": ("unfold", "tab-renta"),
        }),
        ("IV. Retenciones", {
            "fields": (
                "retencion_iva", "retencion_renta",
            ),
            "classes": ("unfold", "tab-retenciones"),
        }),
        ("V. ICE e ISD", {
            "fields": (
                "ice_causado", "pagos_exterior", "isd_causado",
            ),
            "classes": ("unfold", "tab-ice-isd"),
        }),
        ("VI. Patente Municipal", {
            "fields": (
                "base_patente", "patente_municipal",
            ),
            "classes": ("unfold", "tab-patente"),
        }),
    )
    list_editable = (
        "declarado",
    )
    list_display = (
        
        "ejercicio_fiscal",
        "mes",
        "iva_a_pagar",
        "renta_a_pagar",
        "retencion_renta",
        "isd_causado",
        "patente_municipal",
        "cp",
        "declarado"
    )

    list_filter = (
        "regimen",
        "ejercicio_fiscal",
    )

    search_fields = (
        "ruc",
        "razon_social",
    )

    unfold_fieldsets = True


from django.utils.safestring import mark_safe
from django.urls import reverse

def CONTRATO_LABORAL_PDF(obj):
    url = reverse("smartbusinesslaw:pdf_contrato_laboral", args=[obj.id])
    return mark_safe(
        f'<a href="{url}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>'
        f'Contrato Laboral</a>'
    )

CONTRATO_LABORAL_PDF.short_description = "Contrato Laboral"





def ROL_PAGOS_PDF(obj):
    url = reverse("smartbusinesslaw:pdf_rol_pagos", args=[obj.id])
    return mark_safe(
        f'<a href="{url}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span> </a>'
    )

ROL_PAGOS_PDF.short_description = "Rol"




def CHEQUE_SUELDO_PDF(obj):
    url = reverse("smartbusinesslaw:pdf_cheque_sueldo", args=[obj.id])
    return mark_safe(
        f'<a href="{url}" target="_blank">'
        f'<span class="material-symbols-outlined">payments</span></a>'
    )

CHEQUE_SUELDO_PDF.short_description = "Cheque"



# ================================
# I. Identificación del Contrato
# ================================
@register_component
class ContratoIdentificacionComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Identificación del Contrato"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        c = self.instance
        rows = [
            ["Código hash", c.hash_contrato],
            ["Tipo de contrato", c.tipo_contrato],
            ["Fecha de inicio", c.fecha_inicio],
            ["Fecha de fin", c.fecha_fin],
            ["Lugar de trabajo", c.lugar_trabajo],
            ["Tipo de jornada", c.tipo_jornada],
            ["Horas semanales", c.horas_semanales],
            ["Horario", c.horario],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Identificación del Contrato",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


# ================================
# II. Empleador
# ================================
@register_component
class EmpleadorComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Empleador"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        c = self.instance
        rows = [
            ["Razón social", c.empleador_razon_social],
            ["RUC", c.empleador_ruc],
            ["Representante legal", c.empleador_representante_legal],
            ["Domicilio", c.empleador_domicilio],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Datos del Empleador",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


# ================================
# III. Trabajador
# ================================
@register_component
class TrabajadorComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Trabajador"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        c = self.instance
        rows = [
            ["Nombres completos", c.trabajador_nombres],
            ["Cédula / Identificación", c.trabajador_identificacion],
            ["Cargo", c.cargo],
            ["Domicilio", c.trabajador_domicilio],
            ["Nacionalidad", c.trabajador_nacionalidad],
            ["Estado civil", c.trabajador_estado_civil],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Datos del Trabajador",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


# ================================
# IV. Remuneración y Beneficios
# ================================
@register_component
class RemuneracionComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Remuneración"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        c = self.instance
        rows = [
            ["Salario mensual", c.salario_mensual],
            ["Forma de pago", c.forma_pago],
            ["Beneficios adicionales", c.beneficios_adicionales or "Ninguno"],
            ["Décimo tercer sueldo", "Sí" if c.decimo_tercer_sueldo else "No"],
            ["Décimo cuarto sueldo", "Sí" if c.decimo_cuarto_sueldo else "No"],
            ["Aporte IESS", "Sí" if c.afiliacion_iess else "No"],
            ["Vacaciones anuales", c.vacaciones_anuales],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Remuneración y Beneficios",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


# ================================
# V. Cláusulas Legales y Terminación
# ================================
@register_component
class ClausulasComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Cláusulas Legales"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        c = self.instance
        rows = [
            ["Confidencialidad", "Sí" if c.clausula_confidencialidad else "No"],
            ["No competencia", "Sí" if c.clausula_no_competencia else "No"],
            ["Causales de terminación", c.causales_terminacion],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Cláusulas del Contrato",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())



from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ContratoLaboral




@admin.register(ContratoLaboral)
class ContratoLaboralAdmin(ModelAdmin):

    # ----------------------------------
    # Componentes visuales
    # ----------------------------------
    list_sections = [
        ContratoIdentificacionComponent,
        EmpleadorComponent,
        TrabajadorComponent,
        RemuneracionComponent,
        ClausulasComponent,
    ]

    # ----------------------------------
    # Fieldsets (tabs)
    # ----------------------------------
    fieldsets = (

    ("I. Identificación del Contrato", {
        "fields": (
            "hash_contrato",
            "tipo_contrato",
            "fecha_inicio",
            "fecha_fin",
            "duracion_contrato",
            "lugar_trabajo",
            "tipo_jornada",
            "horas_semanales",
            "horario",
        ),
        "classes": ("unfold", "tab-identificacion"),
    }),

    ("II. Empleador", {
        "fields": (
            "empleador_razon_social",
            "empleador_ruc",
            "empleador_representante_legal",
            "empleador_domicilio",
        ),
        "classes": ("unfold", "tab-empleador"),
    }),

    ("III. Trabajador", {
        "fields": (
            "trabajador_nombres",
            "trabajador_identificacion",
            "trabajador_nacionalidad",
            "trabajador_estado_civil",
            "cargo",
            "area_trabajo",
            "funciones",
            "trabajador_domicilio",
        ),
        "classes": ("unfold", "tab-trabajador"),
    }),

    ("IV. Remuneración", {
        "fields": (
            "salario_mensual",
            "forma_pago",
            "beneficios_adicionales",
            "decimo_tercer_sueldo",
            "decimo_cuarto_sueldo",
            "afiliacion_iess",
            "vacaciones_anuales",
        ),
        "classes": ("unfold", "tab-remuneracion"),
    }),

    ("V. Cláusulas Legales", {
        "fields": (
            "clausula_confidencialidad",
            "clausula_no_competencia",
            "causales_terminacion",
        ),
        "classes": ("unfold", "tab-clausulas"),
    }),

    ("VI. Firmas y Formalidades", {
        "fields": (
            "ID_SUT_registro",
            "lugar_firma",
            "fecha_firma",
            "empleador_firma",
            "trabajador_firma",
        ),
        "classes": ("unfold", "tab-firmas"),
    }),
    )


    # ----------------------------------
    # Listado
    # ----------------------------------
    list_display = (
        "trabajador_nombres",
        "tipo_contrato",
        "fecha_inicio",
        "fecha_fin",
        CONTRATO_LABORAL_PDF,
    )

    search_fields = (
        "trabajador_nombres",
        "trabajador_identificacion",
        "empleador_razon_social",
        "hash_contrato",
    )

    list_filter = (
        "tipo_contrato",
        "fecha_inicio",
    )

    readonly_fields = (
        "hash_contrato",
    )

    unfold_fieldsets = True





from django.template.loader import render_to_string
from .models import Nomina


# ================================
# I. Identificación de la Nómina
# ================================
@register_component
class IdentificacionNominaComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Identificación de la Nómina"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        n = self.instance
        rows = [
            ["Mes / Año", f"{n.mes}/{n.anio}"],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Identificación de la Nómina",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


# ================================
# II. Empleador
# ================================
@register_component
class EmpleadorNominaComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Empleador"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        n = self.instance
        rows = [
            ["Nombre del Trabajador", n.contrato.trabajador_nombres],
            ["Razón social", n.razon_social],
            ["RUC", n.ruc_empleador],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Datos del Empleador",
            "table": {"headers": ["Campo", "Detalle"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


# ================================
# III. Remuneración
# ================================
@register_component
class RemuneracionNominaComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Remuneración"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        n = self.instance
        rows = [
            ["Sueldo base", n.sueldo_base],
            ["Horas extra", n.horas_extra or 0],
            ["Otros ingresos", n.otros_ingresos or 0],
            ["Décimo tercero", n.decimo_tercero],
            ["Décimo cuarto", n.decimo_cuarto],
            ["Utilidades", n.utilidades or 0],
            ["Aporte IESS trabajador", n.aporte_iess_trabajador],
            ["Aporte IESS empleador", n.aporte_iess_empleador],
            ["Total ingresos", n.total_ingresos],
            ["Sueldo a pagar", n.sueldo_a_pagar],
        ]
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Remuneración y Beneficios",
            "table": {"headers": ["Concepto", "Valor ($)"], "rows": rows}
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


# ================================
# IV. Documentos PDF
# ================================
@register_component
class DocumentosPDFComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Documentos PDF"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Descargas PDF",
            "pdf_links": [
                ROL_PAGOS_PDF(self.instance),
                CHEQUE_SUELDO_PDF(self.instance),
            ]
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


# ================================
# Admin de Nomina
# ================================

from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Nomina






from .models import Nomina
from django.db.models import Sum, Count

def periodo(obj):
    return f"{obj.mes}-{obj.anio}" 
periodo.short_description = "Período"




@admin.register(Nomina)
class NominaAdmin(ModelAdmin):

    list_sections = [
        IdentificacionNominaComponent,
        EmpleadorNominaComponent,
        RemuneracionNominaComponent,
        DocumentosPDFComponent,
    ]

    # ==========================================================
    # Campos condicionales
    # ==========================================================
    conditional_fields = {
        "otros_ingresos": "recibe_bonificacion == true",
        "decimo_tercero": "recibe_decimo_tercero == true",
        "decimo_cuarto": "recibe_decimo_cuarto == true",
        "utilidades": "recibe_utilidades == true",
        "vacaciones": "recibe_vacaciones == true",
        "descuentos": "recibe_descuento == true",
        "razon_descuento": "recibe_descuento == true",
    }

    # ==========================================================
    # Fieldsets
    # ==========================================================
    fieldsets = (
        ("I. Identificación de la Nómina", {
            "fields": ("mes", "anio", "contrato"),
            "classes": ("unfold", "tab-identificacion"),
        }),
        ("II. Empleador", {
            "fields": ("razon_social", "ruc_empleador"),
            "classes": ("unfold", "tab-empleador"),
        }),
        ("III. Remuneración", {
            "fields": (
                "sueldo_base",
                "horas_extra",

                "recibe_bonificacion",
                "otros_ingresos",

                "recibe_decimo_tercero",
                "decimo_tercero",

                "recibe_decimo_cuarto",
                "decimo_cuarto",

                "recibe_utilidades",
                "utilidades",

                "recibe_vacaciones",
                "vacaciones",

                "recibe_descuento",
                "razon_descuento",
                "descuentos",

                "aporte_iess_trabajador",
                "aporte_iess_empleador",

                "total_ingresos",
                "sueldo_a_pagar",
            ),
            "classes": ("unfold", "tab-remuneracion"),
        }),
    )

    # ==========================================================
    # Listado
    # ==========================================================
    list_display = (
        "contrato",
        "mes",
        "anio",
        "sueldo_base",
        "otros_ingresos",
        "decimo_tercero",
        "decimo_cuarto",
        "utilidades",
        "vacaciones",
        "descuentos",
        "aporte_iess_trabajador",
        "aporte_iess_empleador",
        "sueldo_a_pagar",
        ROL_PAGOS_PDF,
        CHEQUE_SUELDO_PDF,
    )

    search_fields = (
        "contrato__trabajador_nombres",
        "contrato__trabajador_identificacion",
        "razon_social",
    )

    list_filter = ("mes", "anio")

    readonly_fields = (
        "decimo_tercero",
        "decimo_cuarto",
        "utilidades",
        "vacaciones",
        "aporte_iess_trabajador",
        "aporte_iess_empleador",
        "total_ingresos",
        "sueldo_a_pagar",
    )

    unfold_fieldsets = True

    # ==========================================================
    # 🔢 TOTALES (CLAVE)
    # ==========================================================
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        totals = qs.aggregate(
            total_registros=Sum(1),
            total_sueldo_base=Sum("sueldo_base"),
            total_otros_ingresos=Sum("otros_ingresos"),
            total_decimo_tercero=Sum("decimo_tercero"),
            total_decimo_cuarto=Sum("decimo_cuarto"),
            total_utilidades=Sum("utilidades"),
            total_vacaciones=Sum("vacaciones"),
            total_descuentos=Sum("descuentos"),
            total_iess_trabajador=Sum("aporte_iess_trabajador"),
            total_iess_empleador=Sum("aporte_iess_empleador"),
            total_sueldo_pagar=Sum("sueldo_a_pagar"),
        )

        self.totals = {k: v or 0 for k, v in totals.items()}
        self.totals["total_registros"] = qs.count()

        return qs

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["totals"] = getattr(self, "totals", {})
        return super().changelist_view(request, extra_context=extra_context)
