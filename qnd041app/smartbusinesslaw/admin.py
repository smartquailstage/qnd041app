from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib import admin
from .models import SPDP_ActaDelegado, Regulacion ,ClausulaContrato


#SCVS_Estatutos, SRI_RUC, MT_Contratos, IESS_Aportes

from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from unfold.components import BaseComponent, register_component


from .models import Regulacion
from unfold.admin import ModelAdmin, TabularInline


from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr

from .models import CartaNombramiento


def NOMBRAMIENTO_PDF(obj):
    url = reverse("smartbusinesslaw:carta_nombramiento_pdf", args=[obj.id])
    return mark_safe(
        f'<a href="{url}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span>'
        f'Nombramiento</a>'
    )

NOMBRAMIENTO_PDF.short_description = "Nombramiento"

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


@admin.register(CartaNombramiento)
class CartaNombramientoAdmin(ModelAdmin):

    conditional_fields = {
        "duracion_anos": "cargo_designado == 'Presidente'",
        "domicilio_designado": "nacionalidad_designado == 'ecuatoriana'",
    }

    # ==========================================================
    # Fieldsets
    # ==========================================================
    fieldsets = (
        ("I. Datos de la Sociedad", {
            "fields": ("nombre_sociedad", "fecha_constitutiva"),
            "classes": ("unfold", "tab-sociedad"),
        }),
        ("II. Accionista Fundador", {
            "fields": ("nombre_accionista", "cargo_accionista"),
            "classes": ("unfold", "tab-accionista"),
        }),
        ("III. Datos del Designado", {
            "fields": (
                "nombre_designado",
                "cargo_designado",
                "numero_identificacion",
                "codigo_dactilar",
                "nacionalidad_designado",
                "domicilio_designado",
                "duracion_anos",
            ),
            "classes": ("unfold", "tab-designado"),
        }),
        ("IV. Fechas y Control", {
            "fields": ("fecha_emision", "hash_nombramiento", "fecha_acta", "fecha_inscripcion"),
            "classes": ("unfold", "tab-fechas"),
        }),
    )

    # ==========================================================
    # Listado
    # ==========================================================
    list_display = (
        "nombre_designado",
        "cargo_designado",
        "nombre_sociedad",
        "fecha_constitutiva",
        "duracion_anos",
        "fecha_emision",
        NOMBRAMIENTO_PDF,
    )

    search_fields = (
        "nombre_designado",
        "nombre_accionista",
        "nombre_sociedad",
    )

    list_filter = (
        "cargo_designado",
        "fecha_emision",
    )

    readonly_fields = (
        "fecha_emision",
    )


    unfold_fieldsets = True




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
    # Fieldsets clásicos (solo con campos del modelo)
    # ---------------------------
    fieldsets = (
        ('Datos Generales', {
            'fields': ('ruc', 'company_name', 'company_type', 'fiscal_year', 'economic_activity', 'currency'),
            'classes': ('unfold', 'tab-datos-generales'),
        }),

        ('ESTADO DE SITUACIÓN FINACIERA (ESF)', {
            'fields': ('c_1_activo','c_101_activo_corriente', 'c_10101_efectivo_y_equivalentes_de_efectivo', 'c_1010101_caja', 'c_1010102_instituciones_financieras_publicas', 'c_1010103_instituciones_financieras_privadas', 'c_10102_activos_financieros', 'c_1010201_activos_financieros_a_valor_razonable_con_cambios_en_resultados', 'c_101020101_renta_variable', 'c_10102010101_acciones_y_participaciones', 'c_10102010102_cuotas_de_fondos_colectivos', 'c_10102010103_valores_de_titularizacion_de_participacion', 'c_10102010104_unidades_de_participacion', 'c_10102010105_inversiones_en_el_exterior', 'c_10102010106_otros', 'c_101020102_renta_fija', 'c_10102010201_avales', 'c_10102010202_bonos_del_estado', 'c_10102010203_bonos_de_prenda', 'c_10102010204_cedulas_hipotecarias', 'c_10102010205_certificados_financieros', 'c_10102010206_certificados_de_inversion', 'c_10102010207_certificados_de_tesoreria', 'c_10102010208_certificados_de_deposito', 'c_10102010209_cupones', 'c_10102010210_depositos_a_plazo', 'c_10102010211_letras_de_cambio', 'c_10102010212_notas_de_credito', 'c_10102010213_obligaciones', 'c_10102010214_facturas_comerciales_negociables', 'c_10102010215_overnights', 'c_10102010216_obligaciones_convertibles_en_acciones', 'c_10102010217_papel_comercial', 'c_10102010218_pagares', 'c_10102010219_polizas_de_acumulacion', 'c_10102010220_titulos_del_banco_central', 'c_10102010221_valores_de_titularizacion', 'c_10102010222_inversiones_en_el_exterior', 'c_10102010223_otros', 'c_101020103_derivados', 'c_10102010301_forward', 'c_10102010302_futuros', 'c_10102010303_opciones', 'c_10102010304_otros', 'c_1010202_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado_integral', 'c_101020201_renta_variable', 'c_10102020101_acciones_y_participaciones', 'c_10102020102_cuotas_de_fondos_colectivos', 'c_10102020103_unidades_de_participacion', 'c_10102020104_valores_de_titularizacion_de_participacion', 'c_10102020105_inversiones_en_el_exterior', 'c_10102020106_otros', 'c_101020202_renta_fija', 'c_10102020201_avales', 'c_10102020202_bonos_del_estado', 'c_10102020203_bonos_de_prenda', 'c_10102020204_cedulas_hipotecarias', 'c_10102020205_certificados_financieros', 'c_10102020206_certificados_de_inversion', 'c_10102020207_certificados_de_tesoreria', 'c_10102020208_certificados_de_deposito', 'c_10102020209_cupones', 'c_10102020210_depositos_a_plazo', 'c_10102020211_letras_de_cambio', 'c_10102020212_notas_de_credito', 'c_10102020213_obligaciones', 'c_10102020214_facturas_comerciales_negociables', 'c_10102020215_overnights', 'c_10102020216_obligaciones_convertibles_en_acciones', 'c_10102020217_papel_comercial', 'c_10102020218_pagares', 'c_10102020219_polizas_de_acumulacion', 'c_10102020220_titulos_del_banco_central', 'c_10102020221_valores_de_titularizacion', 'c_10102020222_inversiones_en_el_exterior', 'c_10102020223_otros', 'c_1010203_activos_financieros_al_costo_amortizado', 'c_101020302_renta_fija', 'c_10102030201_avales', 'c_10102030202_bonos_del_estado', 'c_10102030203_bonos_de_prenda', 'c_10102030204_cedulas_hipotecarias', 'c_10102030205_certificados_financieros', 'c_10102030206_certificados_de_inversion', 'c_10102030207_certificados_de_tesoreria', 'c_10102030208_certificados_de_deposito', 'c_10102030209_cupones', 'c_10102030210_depositos_a_plazo', 'c_10102030211_letras_de_cambio', 'c_10102030212_notas_de_credito', 'c_10102030213_obligaciones', 'c_10102030214_facturas_comerciales_negociables', 'c_10102030215_overnights', 'c_10102030216_obligaciones_convertibles_en_acciones', 'c_10102030217_papel_comercial', 'c_10102030218_pagares', 'c_10102030219_polizas_de_acumulacion', 'c_10102030220_titulos_del_banco_central', 'c_10102030221_valores_de_titularizacion', 'c_10102030222_inversiones_en_el_exterior', 'c_10102030223_otros', 'c_1010204_provision_por_deterioro_de_activos_financieros', 'c_101020401_activos_financieros_a_valor_razonable_con_cambios_en_resultados', 'c_101020402_activos_financieros_al_costo_amortizado', 'c_101020403_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado_integral', 'c_1010205_deudores_comerciales_y_otras_cuentas_por_cobrar_no_relacionados', 'c_101020501_de_actividades_ordinarias_que_generen_intereses', 'c_10102050101_cuentas_y_documentos_a_cobrar_a_clientes', 'c_10102050102_cuentas_y_documentos_a_cobrar_a_terceros', 'c_101020502_de_actividades_ordinarias_que_no_generen_intereses', 'c_10102050201_cuentas_y_documentos_a_cobrar_a_clientes', 'c_10102050202_cuentas_y_documentos_a_cobrar_a_terceros', 'c_10102050203_cuentas_por_cobrar_al_originador', 'c_10102050204_comisiones_por_operaciones_bursatiles', 'c_10102050207_contrato_de_underwriting', 'c_10102050208_por_administracion_y_manejo_de_portafolios_de_terceros', 'c_10102050209_por_administracion_y_manejo_de_fondos_administrados', 'c_10102050210_por_administracion_y_manejo_de_negocios_fiduciarios', 'c_10102050211_por_custodia_y_conservacion_de_valores_materializados', 'c_10102050212_por_custodia_y_conservacion_de_valores_desmaterializados', 'c_10102050213_por_manejo_de_libro_de_acciones_y_accionistas', 'c_10102050214_por_asesoria', 'c_10102050215_dividendos_por_cobrar', 'c_10102050216_intereses_por_cobrar', 'c_10102050217_deudores_por_intermediacion_de_valores', 'c_10102050218_anticipo_a_comitentes', 'c_10102050219_anticipo_a_constructor_por_avance_de_obra', 'c_10102050220_derechos_por_compromiso_de_recompra', 'c_10102050221_otras_cuentas_por_cobrar_no_relacionadas', 'c_1010206_documentos_y_cuentas_por_cobrar_relacionados', 'c_101020601_por_cobrar_a_accionistas', 'c_101020602_por_cobrar_a_companias_relacionadas', 'c_101020603_por_cobrar_a_clientes', 'c_101020604_otras_cuentas_por_cobrar_relacionadas', 'c_1010207_provision_por_cuentas_incobrables_y_deterioro', 'c_10103_inventarios', 'c_1010301_inventarios_de_materia_prima', 'c_1010302_inventarios_de_productos_en_proceso', 'c_1010303_inventarios_de_suministros_o_materiales_a_ser_consumidos_en_el_proceso_de_produccion', 'c_1010304_inventarios_de_suministros_o_materiales_a_ser_consumidos_en_la_prestacion_del_servicio', 'c_1010305_inventarios_de_prod_term_y_mercad_en_almacen_producido_por_la_compania', 'c_1010306_inventarios_de_prod_term_y_mercad_en_almacen_comprado_a_terceros', 'c_1010307_mercaderias_en_transito', 'c_1010308_obras_en_construccion', 'c_1010309_obras_terminadas', 'c_1010310_materiales_o_bienes_para_la_construccion', 'c_1010311_inventarios_repuestos_herramientas_y_accesorios', 'c_1010312_otros_inventarios', 'c_1010313_provision_por_valor_neto_de_realizacion_y_otras_perdidas_en_inventario', 'c_10104_servicios_y_otros_pagos_anticipados', 'c_1010401_seguros_pagados_por_anticipado', 'c_1010402_arriendos_pagados_por_anticipado', 'c_1010403_anticipos_a_proveedores', 'c_1010404_otros_anticipos_entregados', 'c_10105_activos_por_impuestos_corrientes', 'c_1010501_credito_tributario_a_favor_de_la_empresa_iva', 'c_1010502_credito_tributario_a_favor_de_la_empresa_i_r', 'c_1010503_anticipo_de_impuesto_a_la_renta', 'c_10106_activos_corrientes_mantenidos_para_la_venta_y_operaciones_discontinuadas', 'c_10107_construcciones_en_proceso_nic_11_y_secc23_pymes', 'c_10108_otros_activos_corrientes','c_102_activos_no_corrientes', 'c_10201_propiedad_planta_y_equipo', 'c_1020101_terrenos', 'c_1020102_edificios', 'c_1020103_construcciones_en_curso', 'c_1020104_instalaciones', 'c_1020105_muebles_y_enseres', 'c_1020106_maquinaria_y_equipo', 'c_1020107_naves_aereonaves_barcazas_y_similares', 'c_1020108_equipo_de_computacion', 'c_1020109_vehiculos_equipos_de_trasporte_y_equipo_caminero_movil', 'c_1020110_otros_propiedades_planta_y_equipo', 'c_1020111_repuestos_y_herramientas', 'c_1020112_depreciacion_acumulada_propiedades_planta_y_equipo', 'c_1020113_deterioro_acumulado_de_propiedades_planta_y_equipo', 'c_1020114_activos_de_exploracion_y_explotacion', 'c_102011401_activos_de_exploracion_y_explotacion', 'c_102011402_amortizacion_acumulada_de_activos_de_exploracion_y_explotacion', 'c_102011403_deterioro_acumulado_de_activos_de_exploracion_y_explotacion', 'c_10202_propiedades_de_inversion', 'c_1020201_terrenos', 'c_102020101_terrenos', 'c_102020102_derechos_de_uso_sobre_terrenos_subarrendados', 'c_1020202_edificios', 'c_102020201_edificios', 'c_102020202_derechos_de_uso_sobre_edificios_subarrendados', 'c_1020203_depreciacion_acumulada_de_propiedades_de_inversion', 'c_1020204_deterioro_acumulado_de_propiedades_de_inversion', 'c_10203_activos_biologicos', 'c_1020301_animales_vivos_en_crecimiento', 'c_1020302_animales_vivos_en_produccion', 'c_1020303_plantas_en_crecimiento', 'c_1020304_plantas_en_produccion', 'c_1020305_depreciacion_acumulada_de_activos_biologicos', 'c_1020306_deterioro_acumulado_de_activos_biologicos', 'c_10204_activo_intangible', 'c_1020401_plusvalias', 'c_1020402_marcas_patentes_derechos_de_llave_cuotas_patrimoniales_y_otros_similares', 'c_1020403_concesiones_y_licencias', 'c_1020404_activos_de_exploracion_y_explotacion', 'c_1020405_amortizacion_acumulada_de_activos_intangible', 'c_1020406_deterioro_acumulado_de_activo_intangible', 'c_1020407_otros_intangibles', 'c_10205_activos_por_impuestos_diferidos', 'c_10206_activos_financieros_no_corrientes', 'c_1020601_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado_integral', 'c_1020602_provision_por_deterioro_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado_integral', 'c_1020603_activos_financieros_a_costo_amortizado', 'c_1020604_provision_por_deterioro_de_activos_financieros_a_costo_amortizado', 'c_1020605_activos_financieros_a_valor_razonable_con_cambios_en_resultados', 'c_1020606_provision_por_deterioro_de_activos_financieros_a_valor_razonable_con_cambios_en_resultados', 'c_10207_derecho_de_uso_por_activos_arrendados', 'c_1020701_depreciacion_acumulada_de_activos_provenientes_por_derechos_de_uso', 'c_1020702_deterioro_acumulado_de_activos_provenientes_por_derechos_de_uso', 'c_1020703_derecho_de_uso_por_activos_arrendados', 'c_10208_otros_activos_no_corrientes', 'c_1020801_derechos_fiduciarios', 'c_1020802_depositos_en_garantia', 'c_1020803_depositos_en_garantia_por_operaciones_bursatiles', 'c_1020805_acciones_del_deposito_centralizado_de_valores', 'c_1020806_inversiones_subsidiarias', 'c_1020807_inversiones_asociadas', 'c_1020808_inversiones_negocios_conjuntos', 'c_1020809_otras_inversiones', 'c_1020810_provision_valuacion_de_inversiones', 'c_1020811_otros_activos_no_corrientes', 'c_10209_documentos_y_cuentas_por_cobrar_no_relacionados', 'c_1020901_cuentas_y_documentos_a_cobrar_a_clientes', 'c_1020902_cuentas_y_documentos_a_cobrar_a_terceros', 'c_1020903_otras_cuentas_por_cobrar_no_relacionadas', 'c_10210_documentos_y_cuentas_por_cobrar_relacionados', 'c_1021001_por_cobrar_a_accionistas', 'c_1021002_por_cobrar_a_companias_relacionadas', 'c_1021003_por_cobrar_a_clientes', 'c_1021004_otras_cuentas_por_cobrar_relacionadas','c_2_pasivo','c_201_pasivo_corriente', 'c_20101_pasivos_financieros_a_valor_razonable_con_cambios_en_resultados', 'c_20102_pasivos_por_contratos_de_arrendamiento', 'c_20103_cuentas_y_documentos_por_pagar', 'c_2010301_locales', 'c_201030101_prestamos', 'c_201030102_proveedores', 'c_201030103_otras', 'c_2010302_del_exterior', 'c_201030201_prestamos', 'c_201030202_proveedores', 'c_201030203_otras', 'c_20104_obligaciones_con_instituciones_financieras', 'c_2010401_locales', 'c_2010402_del_exterior', 'c_20105_provisiones', 'c_2010501_locales', 'c_2010502_del_exterior', 'c_20106_porcion_corriente_de_valores_emitidos', 'c_2010601_obligaciones', 'c_2010602_papel_comercial', 'c_2010603_valores_de_titularizacion', 'c_2010604_otros', 'c_2010605_intereses_por_pagar', 'c_20107_otras_obligaciones_corrientes', 'c_2010701_con_la_administracion_tributaria', 'c_2010702_impuesto_a_la_renta_por_pagar_del_ejercicio', 'c_2010703_con_el_iess', 'c_2010704_por_beneficios_de_ley_a_empleados', 'c_2010705_participacion_trabajadores_por_pagar_del_ejercicio', 'c_2010706_dividendos_por_pagar', 'c_2010707_otros', 'c_20108_cuentas_por_pagar_a_relacionadas', 'c_2010801_locales', 'c_201080101_prestamos_de_accionistas', 'c_201080102_prestamos_de_companias_relacionadas', 'c_201080103_proveedores', 'c_201080104_otros', 'c_2010802_del_exterior', 'c_201080201_prestamos_de_accionistas', 'c_201080202_prestamos_de_companias_relacionadas', 'c_201080203_proveedores', 'c_201080204_otros', 'c_20109_otros_pasivos_financieros', 'c_20110_anticipos', 'c_2011001_anticipos_de_clientes', 'c_2011002_otros_anticipos_recibidos', 'c_20111_pasivos_directamente_asociados_con_los_activos_no_corrientes_y_operaciones_discontinuadas', 'c_20112_porcion_corriente_de_provisiones_por_beneficios_a_empleados', 'c_2011201_jubilacion_patronal', 'c_2011202_otros_beneficios_para_los_empleados', 'c_20113_otros_pasivos_corrientes', 'c_2011301_comisiones_por_pagar', 'c_2011302_por_operaciones_bursatiles', 'c_2011303_por_custodia', 'c_2011304_por_administracion', 'c_2011305_otras_comisiones', 'c_2011306_sanciones_y_multas', 'c_2011307_indemnizaciones', 'c_2011308_obligaciones_judiciales', 'c_2011309_acreedores_por_intermediacion', 'c_2011310_obligacion_por_compromiso_de_recompra', 'c_2011311_por_contratos_de_underwriting', 'c_2011312_otros', 'c_20114_pasivos_financieros_al_costo_amortizado','c_202_pasivo_no_corriente', 'c_20201_pasivos_por_contratos_de_arrendamiento', 'c_20202_cuentas_y_documentos_por_pagar', 'c_2020201_locales', 'c_202020101_prestamos', 'c_202020102_proveedores', 'c_202020103_otras', 'c_2020202_del_exterior', 'c_202020201_prestamos', 'c_202020202_proveedores', 'c_202020203_otras', 'c_20203_obligaciones_con_instituciones_financieras', 'c_2020301_locales', 'c_2020302_del_exterior', 'c_20204_cuentas_por_pagar_a_relacionadas', 'c_2020401_locales', 'c_202040101_prestamos_de_accionistas', 'c_202040102_prestamos_de_companias_relacionadas', 'c_202040103_proveedores', 'c_202040104_otros', 'c_2020402_del_exterior', 'c_202040201_prestamos_de_accionistas', 'c_202040202_prestamos_de_companias_relacionadas', 'c_202040203_proveedores', 'c_202040204_otros', 'c_20205_porcion_no_corriente_de_valores_emitidos', 'c_2020501_obligaciones', 'c_2020502_papel_comercial', 'c_2020503_valores_de_titularizacion', 'c_2020504_otros', 'c_2020505_intereses_por_pagar', 'c_20206_anticipos', 'c_2020601_anticipos_de_clientes', 'c_2020602_otros_anticipos_recibidos', 'c_20207_provisiones_por_beneficios_a_empleados', 'c_2020701_jubilacion_patronal', 'c_2020702_otros_beneficios_no_corrientes_para_los_empleados', 'c_20208_otras_provisiones', 'c_20209_pasivo_diferido', 'c_2020901_ingresos_diferidos', 'c_2020902_pasivos_por_impuestos_diferidos', 'c_20210_otros_pasivos_no_corrientes','c_3_patrimonio_neto','c_30_patrimonio_neto_atribuible_a_los_propietarios_de_la_controladora','c_301_capital', 'c_30101_capital_suscrito_o_asignado', 'c_30102_capital_suscrito_no_pagado_acciones_en_tesoreria', 'c_30103_fondo_patrimonial', 'c_30104_patrimonio_de_los_negocios_fiduciarios', 'c_30105_patrimonio_de_los_fondos_de_inversion', 'c_3010501_patrimonio_del_fondo_administrado', 'c_3010502_patrimonio_del_fondo_colectivo','c_302_aportes_de_socios_o_accionistas_para_futura_capitalizacion','c_303_prima_por_emision_primaria_de_acciones','c_304_reservas', 'c_30401_reserva_legal', 'c_30402_reservas_facultativa_y_estatutaria',
            'c_305_otros_resultados_integrales', 'c_30501_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado_integral', 'c_30502_superavit_por_revaluacion_de_propiedades_planta_y_equipo', 'c_30503_superavit_por_revaluacion_de_activos_intangibles', 'c_30504_otros_superavit_por_revaluacion','c_306_resultados_acumulados', 'c_30601_ganancias_acumuladas', 'c_30602_perdidas_acumuladas', 'c_30603_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif', 'c_30604_reserva_de_capital', 'c_30605_reserva_por_donaciones', 'c_30606_reserva_por_valuacion', 'c_30607_superavit_por_revaluacion_de_inversiones','c_307_resultados_del_ejercicio', 'c_30701_ganancia_neta_del_periodo', 'c_30702_perdida_neta_del_periodo','c_31_participacion_controladora',
            ),
            'classes': ('unfold', 'tab-anexos-scvs'),
        }),

        ('ESTADO DE RESULTADO INTEGRAL (ERI) ', {
                    'fields': (
                    'c_401_ingresos_de_actividades_ordinarias', 'c_40101_venta_de_bienes', 'c_40102_prestacion_de_servicios', 'c_4010201_ingresos_por_asesoria', 'c_4010202_ingresos_por_estructuracion_de_oferta_publica_de_valores', 'c_4010203_ingresos_por_estructuracion_de_negocios_fiduciarios', 'c_4010204_otros', 'c_40103_contratos_de_construccion', 'c_40104_subvenciones_del_gobierno', 'c_40105_regalias', 'c_40106_intereses', 'c_4010601_intereses_generados_por_ventas_a_credito', 'c_4010602_intereses_y_rendimientos_financieros', 'c_4010603_otros_intereses_generados', 'c_40107_dividendos', 'c_40108_ganancia_por_medicion_a_valor_razonable_de_activos_biologicos', 'c_40109_ingresos_por_comisiones_prestacion_de_servicios_custodia_registro_compensacion_y_liquidacion', 'c_4010901_comisiones_ganadas_por_intermediacion_de_valores', 'c_401090101_por_operaciones_bursatiles', 'c_401090103_por_contratos_de_underwriting', 'c_401090104_por_comision_en_operaciones', 'c_401090105_por_inscripciones', 'c_401090106_por_mantenimiento_de_inscripcion', 'c_4010902_por_prestacion_de_servicios_de_administracion_y_manejo', 'c_401090201_portafolio_de_terceros', 'c_401090202_fondos_administrados', 'c_401090203_fondos_colectivos', 'c_401090204_titularizacion', 'c_401090205_fideicomisos_mercantiles', 'c_401090206_encargos_fiduciarios', 'c_401090207_por_calificacion_de_riesgo', 'c_401090208_por_representacion_de_obligacionistas', 'c_4010903_custodia_registro_compensacion_y_liquidacion', 'c_401090301_custodia_valores_materializados', 'c_401090302_custodia_valores_desmaterializados', 'c_401090303_compensacion_y_liquidacion_de_valores', 'c_401090304_otros', 'c_40110_ingresos_financieros', 'c_4011001_dividendos', 'c_4011002_intereses_financieros', 'c_4011003_ganancia_en_inversiones_en_asociadas_subsidiarias_y_otras', 'c_4011004_valuacion_de_instrumentos_financieros_a_valor_razonable_con_cambio_en_resultados', 'c_4011005_ganancia_en_venta_de_titulos_valores', 'c_4011006_otros_ingresos_financieros', 'c_40112_descuento_en_ventas', 'c_40113_devoluciones_en_ventas', 'c_40114_bonificacion_en_producto', 'c_40115_otras_rebajas_comerciales', 'c_40116_utilidad_en_cambio', 'c_402_ganancia_bruta', 'c_403_otros_ingresos', 'c_40301_ganancia_en_venta_de_propiedad_planta_y_equipo', 'c_40302_ganancia_en_venta_de_activos_biologicos', 'c_40303_otros', 'c_501_costo_de_ventas_y_produccion', 'c_50101_materiales_utilizados_o_productos_vendidos', 'c_5010101_inventario_inicial_de_bienes_no_producidos_por_la_compania', 'c_5010102_compras_netas_locales_de_bienes_no_producidos_por_la_compania', 'c_5010103_importaciones_de_bienes_no_producidos_por_la_compania', 'c_5010104_inventario_final_de_bienes_no_producidos_por_la_compania', 'c_5010105_inventario_inicial_de_materia_prima', 'c_5010106_compras_netas_locales_de_materia_prima', 'c_5010107_importaciones_de_materia_prima', 'c_5010108_inventario_final_de_materia_prima', 'c_5010109_inventario_inicial_de_productos_en_proceso', 'c_5010110_inventario_final_de_productos_en_proceso', 'c_5010111_inventario_inicial_productos_terminados', 'c_5010112_inventario_final_de_productos_terminados', 'c_50102_mano_de_obra_directa', 'c_5010201_sueldos_y_beneficios_sociales', 'c_5010202_gastos_planes_de_beneficios_a_empleados', 'c_50103_mano_de_obra_indirecta', 'c_5010301_sueldos_y_beneficios_sociales', 'c_5010302_gasto_planes_de_beneficios_a_empleados', 'c_50104_otros_costos_indirectos_de_fabricacion', 'c_5010401_depreciacion_propiedades_planta_y_equipo', 'c_5010402_deterioro_o_perdidas_de_activos_biologicos', 'c_5010403_deterioro_de_propiedad_planta_y_equipo', 'c_5010404_efecto_valor_neto_de_realizacion_de_inventarios', 'c_5010405_gasto_por_garantias_en_venta_de_productos_o_servicios', 'c_5010406_mantenimiento_y_reparaciones', 'c_5010407_suministros_materiales_y_repuestos', 'c_5010408_otros_costos_de_produccion', 'c_50105_costos_de_contratos_de_construcciones', 'c_5010501_costos_de_acuerdo_a_porcentajes_o_grados_de_terminacion', 'c_502_gastos', 'c_50201_gastos_de_venta', 'c_5020101_sueldos_salarios_y_demas_remuneraciones', 'c_5020102_aportes_a_la_seguridad_social_incluido_fondo_de_reserva', 'c_5020103_beneficios_sociales_e_indemnizaciones', 'c_5020104_gasto_planes_de_beneficios_a_empleados', 'c_5020105_honorarios_comisiones_y_dietas_a_personas_naturales', 'c_5020106_remuneraciones_a_otros_trabajadores_autonomos', 'c_5020107_honorarios_a_extranjeros_por_servicios_ocasionales', 'c_5020108_mantenimiento_y_reparaciones', 'c_5020109_arrendamiento', 'c_5020110_comisiones', 'c_5020111_promocion_y_publicidad', 'c_5020112_combustibles', 'c_5020113_lubricantes', 'c_5020114_seguros_y_reaseguros_primas_y_cesiones', 'c_5020115_transporte', 'c_5020116_gastos_de_gestion_agasajos_a_accionistas_trabajadores_y_clientes', 'c_5020117_gastos_de_viaje', 'c_5020118_agua_energia_luz_y_telecomunicaciones', 'c_5020119_notarios_y_registradores_de_la_propiedad_o_mercantiles', 'c_5020120_depreciaciones', 'c_502012001_propiedades_planta_y_equipo', 'c_502012002_propiedades_de_inversion', 'c_502012003_activos_por_derecho_de_uso', 'c_5020121_amortizaciones', 'c_502012101_intangibles', 'c_502012102_otros_activos', 'c_5020122_gasto_deterioro', 'c_502012201_propiedades_planta_y_equipo', 'c_502012202_inventarios', 'c_502012203_instrumentos_financieros', 'c_502012204_intangibles', 'c_502012205_cuentas_por_cobrar', 'c_502012206_otros_activos', 'c_502012207_derechos_de_uso_por_activos_arrendados', 'c_5020123_gastos_por_cantidades_anormales_de_utilizacion_en_el_proceso_de_produccion', 'c_502012301_mano_de_obra', 'c_502012302_materiales', 'c_502012303_costos_de_produccion', 'c_5020124_gasto_por_reestructuracion', 'c_5020125_valor_neto_de_realizacion_de_inventarios', 'c_5020126_gasto_impuesto_a_la_renta_activos_y_pasivos_diferidos', 'c_5020127_suministros_y_materiales', 'c_5020128_otros_gastos', 'c_50202_gastos_administrativos', 'c_5020201_sueldos_salarios_y_demas_remuneraciones', 'c_5020202_aportes_a_la_seguridad_social_incluido_fondo_de_reserva', 'c_5020203_beneficios_sociales_e_indemnizaciones', 'c_5020204_gasto_planes_de_beneficios_a_empleados', 'c_5020205_honorarios_comisiones_y_dietas_a_personas_naturales', 'c_5020206_remuneraciones_a_otros_trabajadores_autonomos', 'c_5020207_honorarios_a_extranjeros_por_servicios_ocasionales', 'c_5020208_mantenimiento_y_reparaciones', 'c_5020209_arrendamiento', 'c_5020210_comisiones', 'c_5020211_promocion_y_publicidad', 'c_5020212_combustibles', 'c_5020213_lubricantes', 'c_5020214_seguros_y_reaseguros_primas_y_cesiones', 'c_5020215_transporte', 'c_5020216_gastos_de_gestion_agasajos_a_accionistas_trabajadores_y_clientes', 'c_5020217_gastos_de_viaje', 'c_5020218_agua_energia_luz_y_telecomunicaciones', 'c_5020219_notarios_y_registradores_de_la_propiedad_o_mercantiles', 'c_5020220_impuestos_contribuciones_y_otros', 'c_5020221_depreciaciones', 'c_502022101_propiedades_planta_y_equipo', 'c_502022102_propiedades_de_inversion', 'c_502022103_activos_por_derecho_de_uso', 'c_5020222_amortizaciones', 'c_502022201_intangibles', 'c_502022202_otros_activos', 'c_5020223_gasto_deterioro', 'c_502022301_propiedades_planta_y_equipo', 'c_502022302_inventarios', 'c_502022303_instrumentos_financieros', 'c_502022304_intangibles', 'c_502022305_cuentas_por_cobrar', 'c_502022306_otros_activos', 'c_502022307_derechos_de_uso_por_activos_arrendados', 'c_5020224_gastos_por_cantidades_anormales_de_utilizacion_en_el_proceso_de_produccion', 'c_502022401_mano_de_obra', 'c_502022402_materiales', 'c_502022403_costos_de_produccion', 'c_5020225_gasto_por_reestructuracion', 'c_5020226_valor_neto_de_realizacion_de_inventarios', 'c_5020227_gasto_impuesto_a_la_renta_activos_y_pasivos_diferidos', 'c_5020228_suministros_y_materiales', 'c_5020229_otros_gastos', 'c_50203_gastos_financieros', 'c_5020301_intereses', 'c_502030101_intereses_por_prestamos', 'c_502030102_intereses_por_arrendamientos', 'c_502030103_intereses_por_valores_emitidos', 'c_502030104_otros_intereses', 'c_5020302_comisiones', 'c_502030201_comisiones_pagadas_por_intermediacion_de_valores', 'c_50203020101_por_operaciones_bursatiles', 'c_50203020103_por_contratos_de_underwriting', 'c_50203020104_por_comision_en_operaciones', 'c_50203020105_por_inscripciones', 'c_50203020106_por_mantenimiento_de_inscripcion', 'c_5020303_por_prestacion_de_servicios_de_administracion_y_manejo', 'c_502030301_portafolio_de_terceros', 'c_502030302_fondos_administrados', 'c_502030303_fondos_colectivos', 'c_502030304_titularizacion', 'c_502030305_fideicomisos_mercantiles', 'c_502030306_encargos_fiduciarios', 'c_502030307_por_calificacion_de_riesgo', 'c_502030308_por_representacion_de_obligacionistas', 'c_5020304_custodia_registro_compensacion_y_liquidacion', 'c_502030401_custodia_valores_materializados', 'c_502030402_custodia_valores_desmaterializados', 'c_502030403_compensacion_y_liquidacion_de_valores', 'c_502030404_otros', 'c_5020305_gastos_por_servicios_de_asesoria_y_estructuracion', 'c_502030501_por_asesoria', 'c_502030502_por_estructuracion_de_oferta_publica_de_valores', 'c_502030503_por_estructuracion_de_negocios_fiduciarios', 'c_502030504_otros', 'c_5020306_gastos_de_financiamiento_de_activos', 'c_5020307_diferencia_en_cambio', 'c_5020308_valuacion_de_instrumentos_financieros_a_valor_razonable_con_cambio_en_resultados', 'c_5020309_perdida_en_venta_de_titulos_valores', 'c_5020310_perdida_en_venta_de_propiedad_planta_y_equipo', 'c_5020311_perdida_en_venta_de_activos_biologicos', 'c_5020312_otros_gastos_financieros', 'c_50204_otros_gastos', 'c_5020401_perdida_en_inversiones_en_asociadas_subsidiarias_y_otras', 'c_5020402_otros', 'c_600_ganancia_perdida_antes_de_15_a_trabajadores_e_impuesto_a_la_renta_de_operaciones_continuadas', 'c_601_15_participacion_trabajadores', 'c_602_ganancia_perdida_antes_de_impuestos', 'c_603_impuesto_a_la_renta_causado', 'c_604_ganancia_perdida_de_operaciones_continuadas_antes_del_impuesto_diferido', 'c_605_gasto_por_impuesto_diferido', 'c_606_ingreso_por_impuesto_diferido', 'c_607_ganancia_perdida_de_operaciones_continuadas', 'c_700_ingresos_por_operaciones_discontinuadas', 'c_701_gastos_por_operaciones_discontinuadas', 'c_702_ganancia_perdida_antes_de_15_a_trabajadores_e_impuesto_a_la_renta_de_operaciones_discontinuadas', 'c_703_15_participacion_trabajadores', 'c_704_ganancia_perdida_antes_de_impuestos_de_operaciones_discontinuadas', 'c_705_impuesto_a_la_renta_causado', 'c_706_ganancia_perdida_de_operaciones_discontinuadas', 'c_707_ganancia_perdida_neta_del_periodo', 'c_800_otro_resultado_integral', 'c_80001_componentes_del_otro_resultado_integral', 'c_80002_diferencia_de_cambio_por_conversion', 'c_80003_valuacion_de_activos_financieros_a_valor_razonable_con_cambio_en_otro_resultado_integral', 'c_80004_ganancias_por_revaluacion_de_propiedades_planta_y_equipo', 'c_80005_ganancias_perdidas_actuariales_por_planes_de_beneficios_definidos', 'c_80006_reversion_del_deterioro_perdida_por_deterioro_de_un_activo_revaluado', 'c_80007_participacion_de_otro_resultado_integral_de_asociadas', 'c_80008_impuesto_sobre_las_ganancias_relativo_a_otro_resultado_integral', 'c_80009_otros_detallar_en_notas', 'c_801_resultado_integral_total_del_ano', 'c_80101_propietarios_de_la_controladora', 'c_80102_participacion_no_controladora_informativo',
                    ),
                    'classes': ('unfold', 'tab-anexos-scvs'),
        }),


        ('ESTADO FLUJO EFECTIVO (EFE)', {
            'fields': (

            'c_95_incremento_neto_disminucion_en_el_efectivo_y_equivalentes_al_efectivo_antes_del_efecto_de_los_cambios_en_la_tasa_de_cambio', 'c_9501_flujos_de_efectivo_procedentes_de_utilizados_en_actividades_de_operacion', 'c_950101_clases_de_cobros_por_actividades_de_operacion', 'c_95010101_cobros_procedentes_de_las_ventas_de_bienes_y_prestacion_de_servicios', 'c_95010102_cobros_procedentes_de_regalias_cuotas_comisiones_y_otros_ingresos_de_actividades_ordinarias', 'c_95010103_cobros_procedentes_de_contratos_mantenidos_con_propositos_de_intermediacion_o_para_negociar', 'c_95010104_cobros_procedentes_de_primas_y_prestaciones_anualidades_y_otros_beneficios_de_polizas_suscritas', 'c_95010105_otros_cobros_por_actividades_de_operacion', 'c_950102_clases_de_pagos_por_actividades_de_operacion', 'c_95010201_pagos_a_proveedores_por_el_suministro_de_bienes_y_servicios', 'c_95010202_pagos_procedentes_de_contratos_mantenidos_para_intermediacion_o_para_negociar', 'c_95010203_pagos_a_y_por_cuenta_de_los_empleados', 'c_95010204_pagos_por_primas_y_prestaciones_anualidades_y_otras_obligaciones_derivadas_de_las_polizas_suscritas', 'c_95010205_otros_pagos_por_actividades_de_operacion', 'c_950103_dividendos_pagados', 'c_950104_dividendos_recibidos', 'c_950105_intereses_pagados', 'c_950106_intereses_recibidos', 'c_950107_impuestos_a_las_ganancias_pagados', 'c_950108_otras_entradas_salidas_de_efectivo', 'c_9502_flujos_de_efectivo_procedentes_de_utilizados_en_actividades_de_inversion', 'c_950201_efectivo_procedentes_de_la_venta_de_acciones_en_subsidiarias_u_otros_negocios', 'c_950202_efectivo_utilizado_para_adquirir_acciones_en_subsidiarias_u_otros_negocios_para_tener_el_control', 'c_950203_efectivo_utilizado_en_la_compra_de_participaciones_no_controladoras', 'c_950204_otros_cobros_por_la_venta_de_acciones_o_instrumentos_de_deuda_de_otras_entidades', 'c_950205_otros_pagos_para_adquirir_acciones_o_instrumentos_de_deuda_de_otras_entidades', 'c_950206_otros_cobros_por_la_venta_de_participaciones_en_negocios_conjuntos', 'c_950207_otros_pagos_para_adquirir_participaciones_en_negocios_conjuntos', 'c_950208_importes_procedentes_por_la_venta_de_propiedades_planta_y_equipo', 'c_950209_adquisiciones_de_propiedades_planta_y_equipo', 'c_950210_importes_procedentes_de_ventas_de_activos_intangibles', 'c_950211_compras_de_activos_intangibles', 'c_950212_importes_procedentes_de_otros_activos_a_largo_plazo', 'c_950213_compras_de_otros_activos_a_largo_plazo', 'c_950214_importes_procedentes_de_subvenciones_del_gobierno', 'c_950215_anticipos_de_efectivo_efectuados_a_terceros', 'c_950216_cobros_procedentes_del_reembolso_de_anticipos_y_prestamos_concedidos_a_terceros', 'c_950217_pagos_derivados_de_contratos_de_futuro_a_termino_de_opciones_y_de_permuta_financiera', 'c_950218_cobros_procedentes_de_contratos_de_futuro_a_termino_de_opciones_y_de_permuta_financiera', 'c_950219_dividendos_recibidos', 'c_950220_intereses_recibidos', 'c_950221_otras_entradas_salidas_de_efectivo', 'c_9503_flujos_de_efectivo_procedentes_de_utilizados_en_actividades_de_financiacion', 'c_950301_aporte_en_efectivo_por_aumento_de_capital', 'c_950302_financiamiento_por_emision_de_titulos_valores', 'c_950303_pagos_por_adquirir_o_rescatar_las_acciones_de_la_entidad', 'c_950304_financiacion_por_prestamos_a_largo_plazo', 'c_950305_pagos_de_prestamos', 'c_950306_pagos_de_pasivos_por_arrendamientos_financieros', 'c_950307_importes_procedentes_de_subvenciones_del_gobierno', 'c_950308_dividendos_pagados', 'c_950309_intereses_recibidos', 'c_950310_otras_entradas_salidas_de_efectivo', 'c_9504_efectos_de_la_variacion_en_la_tasa_de_cambio_sobre_el_efectivo_y_equivalentes_al_efectivo', 'c_950401_efectos_de_la_variacion_en_la_tasa_de_cambio_sobre_el_efectivo_y_equivalentes_al_efectivo', 'c_9505_incremento_disminucion_neto_de_efectivo_y_equivalentes_al_efectivo', 'c_9506_efectivo_y_equivalentes_al_efectivo_al_principio_del_periodo', 'c_9507_efectivo_y_equivalentes_al_efectivo_al_final_del_periodo', 'c_96_ganancia_perdida_antes_de_15_a_trabajadores_e_impuesto_a_la_renta', 'c_97_ajuste_por_partidas_distintas_al_efectivo', 'c_9701_ajustes_por_gasto_de_depreciacion_y_amortizacion', 'c_9702_ajustes_por_gastos_por_deterioro_reversiones_por_deterioro_reconocidas_en_los_resultados_del_periodo', 'c_9703_perdida_ganancia_de_moneda_extranjera_no_realizada', 'c_9704_perdidas_en_cambio_de_moneda_extranjera', 'c_9705_ajustes_por_gastos_en_provisiones', 'c_9706_ajuste_por_participaciones_no_controladoras', 'c_9707_ajuste_por_pagos_basados_en_acciones', 'c_9708_ajustes_por_ganancias_perdidas_en_valor_razonable', 'c_9709_ajustes_por_gasto_por_impuesto_a_la_renta', 'c_9710_ajustes_por_gasto_por_participacion_trabajadores', 'c_9711_otros_ajustes_por_partidas_distintas_al_efectivo', 'c_98_cambios_en_activos_y_pasivos', 'c_9801_incremento_disminucion_en_cuentas_por_cobrar_clientes', 'c_9802_incremento_disminucion_en_otras_cuentas_por_cobrar', 'c_9803_incremento_disminucion_en_anticipos_de_proveedores', 'c_9804_incremento_disminucion_en_inventarios', 'c_9805_incremento_disminucion_en_otros_activos', 'c_9806_incremento_disminucion_en_cuentas_por_pagar_comerciales', 'c_9807_incremento_disminucion_en_otras_cuentas_por_pagar', 'c_9808_incremento_disminucion_en_beneficios_empleados', 'c_9809_incremento_disminucion_en_anticipos_de_clientes',





            ),
            'classes': ('unfold', 'tab-cambios-patrimonio'),
        }),
        ('ESTADO CAMBIO PATRIMONIO (ECP)', {
            'fields': (

                            'c_99_301_saldo_al_final_del_periodo_capital',
                            'c_99_302_saldo_al_final_del_periodo_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_99_303_saldo_al_final_del_periodo_prima_por_emision_primaria_de_acciones',
                            'c_99_30401_saldo_al_final_del_periodo_reserva_legal',
                            'c_99_30402_saldo_al_final_del_periodo_reservas_facultativa_y_estatutaria',
                            'c_99_30501_saldo_al_final_del_periodo_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_99_30502_saldo_al_final_del_periodo_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_99_30503_saldo_al_final_del_periodo_superavit_por_revaluacion_de_activos_intangibles',
                            'c_99_30504_saldo_al_final_del_periodo_otros_superavit_por_revaluacion',
                            'c_99_30601_saldo_al_final_del_periodo_ganancias_acumuladas',
                            'c_99_30602_saldo_al_final_del_periodo_perdidas_acumuladas',
                            'c_99_30603_saldo_al_final_del_periodo_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_99_30604_saldo_al_final_del_periodo_reserva_de_capital',
                            'c_99_30605_saldo_al_final_del_periodo_reserva_por_donaciones',
                            'c_99_30606_saldo_al_final_del_periodo_reserva_por_valuacion',
                            'c_99_30607_saldo_al_final_del_periodo_superavit_por_revaluacion_de_inversiones',
                            'c_99_30701_saldo_al_final_del_periodo_ganancia_neta_del_periodo',
                            'c_99_30702_saldo_al_final_del_periodo_perdida_neta_del_periodo',
                            'c_9901_301_saldo_reexpresado_del_periodo_inmediato_anterior_capital',
                            'c_9901_302_saldo_reexpresado_del_periodo_inmediato_anterior_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_9901_303_saldo_reexpresado_del_periodo_inmediato_anterior_prima_por_emision_primaria_de_acciones',
                            'c_9901_30401_saldo_reexpresado_del_periodo_inmediato_anterior_reserva_legal',
                            'c_9901_30402_saldo_reexpresado_del_periodo_inmediato_anterior_reservas_facultativa_y_estatutaria',
                            'c_9901_30501_saldo_reexpresado_del_periodo_inmediato_anterior_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_9901_30502_saldo_reexpresado_del_periodo_inmediato_anterior_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_9901_30503_saldo_reexpresado_del_periodo_inmediato_anterior_superavit_por_revaluacion_de_activos_intangibles',
                            'c_9901_30504_saldo_reexpresado_del_periodo_inmediato_anterior_otros_superavit_por_revaluacion',
                            'c_9901_30601_saldo_reexpresado_del_periodo_inmediato_anterior_ganancias_acumuladas',
                            'c_9901_30602_saldo_reexpresado_del_periodo_inmediato_anterior_perdidas_acumuladas',
                            'c_9901_30603_saldo_reexpresado_del_periodo_inmediato_anterior_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_9901_30604_saldo_reexpresado_del_periodo_inmediato_anterior_reserva_de_capital',
                            'c_9901_30605_saldo_reexpresado_del_periodo_inmediato_anterior_reserva_por_donaciones',
                            'c_9901_30606_saldo_reexpresado_del_periodo_inmediato_anterior_reserva_por_valuacion',
                            'c_9901_30607_saldo_reexpresado_del_periodo_inmediato_anterior_superavit_por_revaluacion_de_inversiones',
                            'c_9901_30701_saldo_reexpresado_del_periodo_inmediato_anterior_ganancia_neta_del_periodo',
                            'c_9901_30702_saldo_reexpresado_del_periodo_inmediato_anterior_perdida_neta_del_periodo',
                            'c_990101_301_saldo_del_periodo_inmediato_anterior_capital',
                            'c_990101_302_saldo_del_periodo_inmediato_anterior_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_990101_303_saldo_del_periodo_inmediato_anterior_prima_por_emision_primaria_de_acciones',
                            'c_990101_30401_saldo_del_periodo_inmediato_anterior_reserva_legal',
                            'c_990101_30402_saldo_del_periodo_inmediato_anterior_reservas_facultativa_y_estatutaria',
                            'c_990101_30501_saldo_del_periodo_inmediato_anterior_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_990101_30502_saldo_del_periodo_inmediato_anterior_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990101_30503_saldo_del_periodo_inmediato_anterior_superavit_por_revaluacion_de_activos_intangibles',
                            'c_990101_30504_saldo_del_periodo_inmediato_anterior_otros_superavit_por_revaluacion',
                            'c_990101_30601_saldo_del_periodo_inmediato_anterior_ganancias_acumuladas',
                            'c_990101_30602_saldo_del_periodo_inmediato_anterior_perdidas_acumuladas',
                            'c_990101_30603_saldo_del_periodo_inmediato_anterior_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_990101_30604_saldo_del_periodo_inmediato_anterior_reserva_de_capital',
                            'c_990101_30605_saldo_del_periodo_inmediato_anterior_reserva_por_donaciones',
                            'c_990101_30606_saldo_del_periodo_inmediato_anterior_reserva_por_valuacion',
                            'c_990101_30607_saldo_del_periodo_inmediato_anterior_superavit_por_revaluacion_de_inversiones',
                            'c_990101_30701_saldo_del_periodo_inmediato_anterior_ganancia_neta_del_periodo',
                            'c_990101_30702_saldo_del_periodo_inmediato_anterior_perdida_neta_del_periodo',
                            'c_990102_301_cambios_en_politicas_contables_capital',
                            'c_990102_302_cambios_en_politicas_contables_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_990102_303_cambios_en_politicas_contables_prima_por_emision_primaria_de_acciones',
                            'c_990102_30401_cambios_en_politicas_contables_reserva_legal',
                            'c_990102_30402_cambios_en_politicas_contables_reservas_facultativa_y_estatutaria',
                            'c_990102_30501_cambios_en_politicas_contables_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_990102_30502_cambios_en_politicas_contables_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990102_30503_cambios_en_politicas_contables_superavit_por_revaluacion_de_activos_intangibles',
                            'c_990102_30504_cambios_en_politicas_contables_otros_superavit_por_revaluacion',
                            'c_990102_30601_cambios_en_politicas_contables_ganancias_acumuladas',
                            'c_990102_30602_cambios_en_politicas_contables_perdidas_acumuladas',
                            'c_990102_30603_cambios_en_politicas_contables_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_990102_30604_cambios_en_politicas_contables_reserva_de_capital',
                            'c_990102_30605_cambios_en_politicas_contables_reserva_por_donaciones',
                            'c_990102_30606_cambios_en_politicas_contables_reserva_por_valuacion',
                            'c_990102_30607_cambios_en_politicas_contables_superavit_por_revaluacion_de_inversiones',
                            'c_990102_30701_cambios_en_politicas_contables_ganancia_neta_del_periodo',
                            'c_990102_30702_cambios_en_politicas_contables_perdida_neta_del_periodo',
                            'c_990103_301_correccion_de_errores_capital',
                            'c_990103_302_correccion_de_errores_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_990103_303_correccion_de_errores_prima_por_emision_primaria_de_acciones',
                            'c_990103_30401_correccion_de_errores_reserva_legal',
                            'c_990103_30402_correccion_de_errores_reservas_facultativa_y_estatutaria',
                            'c_990103_30501_correccion_de_errores_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_990103_30502_correccion_de_errores_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990103_30503_correccion_de_errores_superavit_por_revaluacion_de_activos_intangibles',
                            'c_990103_30504_correccion_de_errores_otros_superavit_por_revaluacion',
                            'c_990103_30601_correccion_de_errores_ganancias_acumuladas',
                            'c_990103_30602_correccion_de_errores_perdidas_acumuladas',
                            'c_990103_30603_correccion_de_errores_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_990103_30604_correccion_de_errores_reserva_de_capital',
                            'c_990103_30605_correccion_de_errores_reserva_por_donaciones',
                            'c_990103_30606_correccion_de_errores_reserva_por_valuacion',
                            'c_990103_30607_correccion_de_errores_superavit_por_revaluacion_de_inversiones',
                            'c_990103_30701_correccion_de_errores_ganancia_neta_del_periodo',
                            'c_990103_30702_correccion_de_errores_perdida_neta_del_periodo',
                            'c_9902_301_cambios_del_ano_en_el_patrimonio_capital',
                            'c_9902_302_cambios_del_ano_en_el_patrimonio_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_9902_303_cambios_del_ano_en_el_patrimonio_prima_por_emision_primaria_de_acciones',
                            'c_9902_30401_cambios_del_ano_en_el_patrimonio_reserva_legal',
                            'c_9902_30402_cambios_del_ano_en_el_patrimonio_reservas_facultativa_y_estatutaria',
                            'c_9902_30501_cambios_del_ano_en_el_patrimonio_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_9902_30502_cambios_del_ano_en_el_patrimonio_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_9902_30503_cambios_del_ano_en_el_patrimonio_superavit_por_revaluacion_de_activos_intangibles',
                            'c_9902_30504_cambios_del_ano_en_el_patrimonio_otros_superavit_por_revaluacion',
                            'c_9902_30601_cambios_del_ano_en_el_patrimonio_ganancias_acumuladas',
                            'c_9902_30602_cambios_del_ano_en_el_patrimonio_perdidas_acumuladas',
                            'c_9902_30603_cambios_del_ano_en_el_patrimonio_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_9902_30604_cambios_del_ano_en_el_patrimonio_reserva_de_capital',
                            'c_9902_30605_cambios_del_ano_en_el_patrimonio_reserva_por_donaciones',
                            'c_9902_30606_cambios_del_ano_en_el_patrimonio_reserva_por_valuacion',
                            'c_9902_30607_cambios_del_ano_en_el_patrimonio_superavit_por_revaluacion_de_inversiones',
                            'c_9902_30701_cambios_del_ano_en_el_patrimonio_ganancia_neta_del_periodo',
                            'c_9902_30702_cambios_del_ano_en_el_patrimonio_perdida_neta_del_periodo',
                            'c_990201_301_aumento_disminucion_de_capital_social_capital',
                            'c_990201_302_aumento_disminucion_de_capital_social_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_990201_303_aumento_disminucion_de_capital_social_prima_por_emision_primaria_de_acciones',
                            'c_990201_30401_aumento_disminucion_de_capital_social_reserva_legal',
                            'c_990201_30402_aumento_disminucion_de_capital_social_reservas_facultativa_y_estatutaria',
                            'c_990201_30501_aumento_disminucion_de_capital_social_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_990201_30502_aumento_disminucion_de_capital_social_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990201_30503_aumento_disminucion_de_capital_social_superavit_por_revaluacion_de_activos_intangibles',
                            'c_990201_30504_aumento_disminucion_de_capital_social_otros_superavit_por_revaluacion',
                            'c_990201_30601_aumento_disminucion_de_capital_social_ganancias_acumuladas',
                            'c_990201_30602_aumento_disminucion_de_capital_social_perdidas_acumuladas',
                            'c_990201_30603_aumento_disminucion_de_capital_social_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_990201_30604_aumento_disminucion_de_capital_social_reserva_de_capital',
                            'c_990201_30605_aumento_disminucion_de_capital_social_reserva_por_donaciones',
                            'c_990201_30606_aumento_disminucion_de_capital_social_reserva_por_valuacion',
                            'c_990201_30607_aumento_disminucion_de_capital_social_superavit_por_revaluacion_de_inversiones',
                            'c_990201_30701_aumento_disminucion_de_capital_social_ganancia_neta_del_periodo',
                            'c_990201_30702_aumento_disminucion_de_capital_social_perdida_neta_del_periodo',
                            'c_990202_301_aportes_para_futuras_capitalizaciones_capital',
                            'c_990202_302_aportes_para_futuras_capitalizaciones_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_990202_303_aportes_para_futuras_capitalizaciones_prima_por_emision_primaria_de_acciones',
                            'c_990202_30401_aportes_para_futuras_capitalizaciones_reserva_legal',
                            'c_990202_30402_aportes_para_futuras_capitalizaciones_reservas_facultativa_y_estatutaria',
                            'c_990202_30501_aportes_para_futuras_capitalizaciones_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_990202_30502_aportes_para_futuras_capitalizaciones_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990202_30503_aportes_para_futuras_capitalizaciones_superavit_por_revaluacion_de_activos_intangibles',
                            'c_990202_30504_aportes_para_futuras_capitalizaciones_otros_superavit_por_revaluacion',
                            'c_990202_30601_aportes_para_futuras_capitalizaciones_ganancias_acumuladas',
                            'c_990202_30602_aportes_para_futuras_capitalizaciones_perdidas_acumuladas',
                            'c_990202_30603_aportes_para_futuras_capitalizaciones_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_990202_30604_aportes_para_futuras_capitalizaciones_reserva_de_capital',
                            'c_990202_30605_aportes_para_futuras_capitalizaciones_reserva_por_donaciones',
                            'c_990202_30606_aportes_para_futuras_capitalizaciones_reserva_por_valuacion',
                            'c_990202_30607_aportes_para_futuras_capitalizaciones_superavit_por_revaluacion_de_inversiones',
                            'c_990202_30701_aportes_para_futuras_capitalizaciones_ganancia_neta_del_periodo',
                            'c_990202_30702_aportes_para_futuras_capitalizaciones_perdida_neta_del_periodo',
                            'c_990203_301_prima_por_emision_primaria_de_acciones_capital',
                            'c_990203_302_prima_por_emision_primaria_de_acciones_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_990203_303_prima_por_emision_primaria_de_acciones_prima_por_emision_primaria_de_acciones',
                            'c_990203_30401_prima_por_emision_primaria_de_acciones_reserva_legal',
                            'c_990203_30402_prima_por_emision_primaria_de_acciones_reservas_facultativa_y_estatutaria',
                            'c_990203_30501_prima_por_emision_primaria_de_acciones_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_990203_30502_prima_por_emision_primaria_de_acciones_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990203_30503_prima_por_emision_primaria_de_acciones_superavit_por_revaluacion_de_activos_intangibles',
                            'c_990203_30504_prima_por_emision_primaria_de_acciones_otros_superavit_por_revaluacion',
                            'c_990203_30601_prima_por_emision_primaria_de_acciones_ganancias_acumuladas',
                            'c_990203_30602_prima_por_emision_primaria_de_acciones_perdidas_acumuladas',
                            'c_990203_30603_prima_por_emision_primaria_de_acciones_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_990203_30604_prima_por_emision_primaria_de_acciones_reserva_de_capital',
                            'c_990203_30605_prima_por_emision_primaria_de_acciones_reserva_por_donaciones',
                            'c_990203_30606_prima_por_emision_primaria_de_acciones_reserva_por_valuacion',
                            'c_990203_30607_prima_por_emision_primaria_de_acciones_superavit_por_revaluacion_de_inversiones',
                            'c_990203_30701_prima_por_emision_primaria_de_acciones_ganancia_neta_del_periodo',
                            'c_990203_30702_prima_por_emision_primaria_de_acciones_perdida_neta_del_periodo',
                            'c_990204_301_dividendos_capital',
                            'c_990204_302_dividendos_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_990204_303_dividendos_prima_por_emision_primaria_de_acciones',
                            'c_990204_30401_dividendos_reserva_legal',
                            'c_990204_30402_dividendos_reservas_facultativa_y_estatutaria',
                            'c_990204_30501_dividendos_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_990204_30502_dividendos_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990204_30503_dividendos_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990204_30504_dividendos_otros_superavit_por_revaluacion',
                            'c_990204_30601_dividendos_ganancias_acumuladas',
                            'c_990204_30602_dividendos_perdidas_acumuladas',
                            'c_990204_30603_dividendos_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_990204_30604_dividendos_reserva_de_capital',
                            'c_990204_30605_dividendos_reserva_por_donaciones',
                            'c_990204_30606_dividendos_reserva_por_valuacion',
                            'c_990204_30607_dividendos_superavit_por_revaluacion_de_inversiones',
                            'c_990204_30701_dividendos_ganancia_neta_del_periodo',
                            'c_990204_30702_dividendos_perdida_neta_del_periodo',
                            'c_990205_301_transferencia_de_resultados_a_otras_cuentas_patrimoniales_capital',
                            'c_990205_302_transferencia_de_resultados_a_otras_cuentas_patrimoniales_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_990205_303_transferencia_de_resultados_a_otras_cuentas_patrimoniales_prima_por_emision_primaria_de_acciones',
                            'c_990205_30401_transferencia_de_resultados_a_otras_cuentas_patrimoniales_reserva_legal',
                            'c_990205_30402_transferencia_de_resultados_a_otras_cuentas_patrimoniales_reservas_facultativa_y_estatutaria',
                            'c_990205_30501_transferencia_de_resultados_a_otras_cuentas_patrimoniales_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_990205_30502_transferencia_de_resultados_a_otras_cuentas_patrimoniales_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990205_30503_transferencia_de_resultados_a_otras_cuentas_patrimoniales_superavit_por_revaluacion_de_activos_intangibles',
                            'c_990205_30504_transferencia_de_resultados_a_otras_cuentas_patrimoniales_otros_superavit_por_revaluacion',
                            'c_990205_30601_transferencia_de_resultados_a_otras_cuentas_patrimoniales_ganancias_acumuladas',
                            'c_990205_30602_transferencia_de_resultados_a_otras_cuentas_patrimoniales_perdidas_acumuladas',
                            'c_990205_30603_transferencia_de_resultados_a_otras_cuentas_patrimoniales_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_990205_30604_transferencia_de_resultados_a_otras_cuentas_patrimoniales_reserva_de_capital',
                            'c_990205_30605_transferencia_de_resultados_a_otras_cuentas_patrimoniales_reserva_por_donaciones',
                            'c_990205_30606_transferencia_de_resultados_a_otras_cuentas_patrimoniales_reserva_por_valuacion',
                            'c_990205_30607_transferencia_de_resultados_a_otras_cuentas_patrimoniales_superavit_por_revaluacion_de_inversiones',
                            'c_990205_30701_transferencia_de_resultados_a_otras_cuentas_patrimoniales_ganancia_neta_del_periodo',
                            'c_990205_30702_transferencia_de_resultados_a_otras_cuentas_patrimoniales_perdida_neta_del_periodo',
                            'c_990206_301_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_capital',
                            'c_990206_302_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_990206_303_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_prima_por_emision_primaria_de_acciones',
                            'c_990206_30401_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_reserva_legal',
                            'c_990206_30402_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_reservas_facultativa_y_estatutaria',
                            'c_990206_30501_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_990206_30502_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990206_30503_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_superavit_por_revaluacion_de_activos_intangibles',
                            'c_990206_30504_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_otros_superavit_por_revaluacion',
                            'c_990206_30601_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_ganancias_acumuladas',
                            'c_990206_30602_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_perdidas_acumuladas',
                            'c_990206_30603_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_990206_30604_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_reserva_de_capital',
                            'c_990206_30605_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_reserva_por_donaciones',
                            'c_990206_30606_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_reserva_por_valuacion',
                            'c_990206_30607_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_superavit_por_revaluacion_de_inversiones',
                            'c_990206_30701_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_ganancia_neta_del_periodo',
                            'c_990206_30702_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_perdida_neta_del_periodo',
                            'c_990207_301_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_capital',
                            'c_990207_302_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_990207_303_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_prima_por_emision_primaria_de_acciones',
                            'c_990207_30401_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_reserva_legal',
                            'c_990207_30402_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_reservas_facultativa_y_estatutaria',
                            'c_990207_30501_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_990207_30502_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990207_30503_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_superavit_por_revaluacion_de_activos_intangibles',
                            'c_990207_30504_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_otros_superavit_por_revaluacion',
                            'c_990207_30601_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_ganancias_acumuladas',
                            'c_990207_30602_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_perdidas_acumuladas',
                            'c_990207_30603_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_990207_30604_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_reserva_de_capital',
                            'c_990207_30605_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_reserva_por_donaciones',
                            'c_990207_30606_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_reserva_por_valuacion',
                            'c_990207_30607_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_superavit_por_revaluacion_de_inversiones',
                            'c_990207_30701_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_ganancia_neta_del_periodo',
                            'c_990207_30702_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_perdida_neta_del_periodo',
                            'c_990208_301_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_capital',
                            'c_990208_302_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_990208_303_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_prima_por_emision_primaria_de_acciones',
                            'c_990208_30401_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_reserva_legal',
                            'c_990208_30402_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_reservas_facultativa_y_estatutaria',
                            'c_990208_30501_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_990208_30502_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990208_30503_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_superavit_por_revaluacion_de_activos_intangibles',
                            'c_990208_30504_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_otros_superavit_por_revaluacion',
                            'c_990208_30601_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_ganancias_acumuladas',
                            'c_990208_30602_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_perdidas_acumuladas',
                            'c_990208_30603_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_990208_30604_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_reserva_de_capital',
                            'c_990208_30605_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_reserva_por_donaciones',
                            'c_990208_30606_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_reserva_por_valuacion',
                            'c_990208_30607_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_superavit_por_revaluacion_de_inversiones',
                            'c_990208_30701_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_ganancia_neta_del_periodo',
                            'c_990208_30702_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_perdida_neta_del_periodo',
                            'c_990209_301_otros_cambios_detallar_capital',
                            'c_990209_302_otros_cambios_detallar_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_990209_303_otros_cambios_detallar_prima_por_emision_primaria_de_acciones',
                            'c_990209_30401_otros_cambios_detallar_reserva_legal',
                            'c_990209_30402_otros_cambios_detallar_reservas_facultativa_y_estatutaria',
                            'c_990209_30501_otros_cambios_detallar_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_990209_30502_otros_cambios_detallar_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990209_30503_otros_cambios_detallar_superavit_por_revaluacion_de_activos_intangibles',
                            'c_990209_30504_otros_cambios_detallar_otros_superavit_por_revaluacion',
                            'c_990209_30601_otros_cambios_detallar_ganancias_acumuladas',
                            'c_990209_30602_otros_cambios_detallar_perdidas_acumuladas',
                            'c_990209_30603_otros_cambios_detallar_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_990209_30604_otros_cambios_detallar_reserva_de_capital',
                            'c_990209_30605_otros_cambios_detallar_reserva_por_donaciones',
                            'c_990209_30606_otros_cambios_detallar_reserva_por_valuacion',
                            'c_990209_30607_otros_cambios_detallar_superavit_por_revaluacion_de_inversiones',
                            'c_990209_30701_otros_cambios_detallar_ganancia_neta_del_periodo',
                            'c_990209_30702_otros_cambios_detallar_perdida_neta_del_periodo',
                            'c_990210_301_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_capital',
                            'c_990210_302_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_aportes_de_socios_o_accionistas_para_futura_capitalizacion',
                            'c_990210_303_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_prima_por_emision_primaria_de_acciones',
                            'c_990210_30401_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_reserva_legal',
                            'c_990210_30402_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_reservas_facultativa_y_estatutaria',
                            'c_990210_30501_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado',
                            'c_990210_30502_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_superavit_por_revaluacion_de_propiedades_planta_y_equipo',
                            'c_990210_30503_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_superavit_por_revaluacion_de_activos_intangibles',
                            'c_990210_30504_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_otros_superavit_por_revaluacion',
                            'c_990210_30601_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_ganancias_acumuladas',
                            'c_990210_30602_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_perdidas_acumuladas',
                            'c_990210_30603_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif',
                            'c_990210_30604_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_reserva_de_capital',
                            'c_990210_30605_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_reserva_por_donaciones',
                            'c_990210_30606_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_reserva_por_valuacion',
                            'c_990210_30607_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_superavit_por_revaluacion_de_inversiones',
                            'c_990210_30701_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_ganancia_neta_del_periodo',
                            'c_990210_30702_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_perdida_neta_del_periodo',
                            'c_99_30_saldo_al_final_del_periodo',
                            'c_99_31_saldo_al_final_del_periodo',
                            'c_9901_30_saldo_reexpresado_del_periodo_inmediato_anterior',
                            'c_9901_31_saldo_reexpresado_del_periodo_inmediato_anterior',
                            'c_9902_30_cambios_del_ano_en_el_patrimonio',
                            'c_9902_31_cambios_del_ano_en_el_patrimonio',
                            'c_990101_30_saldo_del_periodo_inmediato_anterior',
                            'c_990101_31_saldo_del_periodo_inmediato_anterior',
                            'c_990102_30_cambios_en_politicas_contables',
                            'c_990102_31_cambios_en_politicas_contables',
                            'c_990103_30_correccion_de_errores',
                            'c_990103_31_correccion_de_errores',
                            'c_990201_30_aumento_disminucion_de_capital_social',
                            'c_990201_31_aumento_disminucion_de_capital_social',
                            'c_990202_30_aportes_para_futuras_capitalizaciones',
                            'c_990202_31_aportes_para_futuras_capitalizaciones',
                            'c_990203_30_prima_por_emision_primaria_de_acciones',
                            'c_990203_31_prima_por_emision_primaria_de_acciones',
                            'c_990204_30_dividendos',
                            'c_990204_31_dividendos',
                            'c_990205_30_transferencia_de_resultados_a_otras_cuentas_patrimoniales',
                            'c_990205_31_transferencia_de_resultados_a_otras_cuentas_patrimoniales',
                            'c_990206_30_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta',
                            'c_990206_31_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta',
                            'c_990207_30_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo',
                            'c_990207_31_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo',
                            'c_990208_30_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles',
                            'c_990208_31_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles',
                            'c_990209_30_otros_cambios_detallar',
                            'c_990209_31_otros_cambios_detallar',
                            'c_990210_30_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio',
                            'c_990210_31_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio'

            ),
            'classes': ('unfold', 'tab-flujo-efectivo'),
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
    template_name = "scvs/pdf_acta_junta.html"
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

    inlines = [ClausulaContratoInline]

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


from django.utils.safestring import mark_safe
from django.urls import reverse

def ZIP_BENEFICIARIOS(obj):
    """
    Genera un link para descargar el REBEFICS (beneficiarios finales) en ZIP.
    Funciona de manera anual (no depende del mes).
    """
    # Construir URL del ZIP REBEFICS
    url_zip = reverse(
        'smartbusinesslaw:zip_beneficiarios_finales',
        args=[obj.ruc, obj.ejercicio_fiscal]
    )

    # Retornar link HTML seguro
    return mark_safe(
        f'<a href="{url_zip}" target="_blank">'
        f'<span class="material-symbols-outlined">download</span> Descargar</a>'
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
                "compras_monto_iva", "compras_total",
                "ventas_tipo_id_cliente", "ventas_id_cliente", "ventas_razon_social_cliente",
                "ventas_base_iva_0", "ventas_base_iva", "ventas_porcentaje_iva",
                "ventas_monto_iva", "ventas_total", "ventas_forma_cobro",
                "ventas_compensacion_ley_solidaridad",
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

        ("VIII. Beneficiarios Finales", {
            "fields": (
                "bf_tipo_identificacion",
                "bf_identificacion",
                "bf_primer_nombre",
                "bf_segundo_nombre",
                "bf_primer_apellido",
                "bf_segundo_apellido",
                "bf_fecha_nacimiento",
                "bf_residencia_fiscal",
                "bf_nacionalidad_uno",
                "bf_nacionalidad_dos",
                "bf_provincia",
                "bf_canton",
                "bf_parroquia",
                "bf_calle",
                "bf_numero",
                "bf_interseccion",
                "bf_codigo_postal",
                "bf_referencia",
                "bf_porcentaje_participacion",
                "bf_por_propiedad",
                "bf_por_administracion",
                "bf_por_otros_motivos",
                "distribuyo_dividendos",
                "dividendo_pagado",
                "impuesto_dividendo",
                "socio_tipo_identificacion",
                "socio_identificacion",
                "socio_nombre",
                "socio_tipo_sujeto",
                "socio_porcentaje",
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
