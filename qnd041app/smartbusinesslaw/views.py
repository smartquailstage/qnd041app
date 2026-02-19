from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from .models import SPDP_ActaDelegado
from .models import SCVS_ActasAsamblea


import qrcode
import io
import base64
from django.utils.crypto import get_random_string
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

import io
import base64
import qrcode
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
import weasyprint

from .models import SPDP_ActaDelegado


@staff_member_required
def incidente_pdf(request, delegado_id):
    # Obtener el delegado
    delegado = get_object_or_404(SPDP_ActaDelegado, id=delegado_id)

    # Generar hash único para incidente si aún no existe
    if not delegado.hash_incidente:
        delegado.generate_hash_incidente()  # guarda automáticamente en DB

    # Generar QR basado en el hash del incidente
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=4,
    )
    qr_data = f"INCIDENTE-{delegado.id}-{delegado.hash_incidente}"
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    qr_url = f"data:image/png;base64,{qr_base64}"

    # Renderizar plantilla HTML
    html = render_to_string('spdp/pdf_incidente.html', {
        'delegado': delegado,
        'qr_url': qr_url,
    })

    # Crear respuesta PDF con WeasyPrint
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=incidente_{delegado.id}.pdf'

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')],
        presentational_hints=True
    )

    return response


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=incidente_{delegado.id}.pdf'

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')],
        presentational_hints=True
    )

    return response





import io
import base64
import qrcode
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
import weasyprint

@staff_member_required
def delegado_pdf(request, delegado_id):
    delegado = get_object_or_404(SPDP_ActaDelegado, id=delegado_id)
    
    # -------------------------------
    # 1. Generar hash único si no existe
    # -------------------------------
    if not delegado.hash_incidente:
        delegado.hash_incidente = get_random_string(32)
        delegado.save()

    # -------------------------------
    # 2. Generar QR con el hash
    # -------------------------------
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=4,
    )
    qr_data = f"DELEGADO-{delegado.id}-{delegado.hash_incidente}"
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    qr_url = f"data:image/png;base64,{qr_base64}"

    # -------------------------------
    # 3. Renderizar la plantilla con hash y QR
    # -------------------------------
    html = render_to_string('spdp/delegado/pdf.html', {
        'delegado': delegado,
        'qr_url': qr_url,
    })

    # -------------------------------
    # 4. Crear respuesta PDF
    # -------------------------------
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=Delegado_{delegado.nombre_delegado}_{delegado.fecha_nombramiento}.pdf'

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')],
        presentational_hints=True
    )

    return response



from .models import Regulacion

@staff_member_required
def regulacion_pdf(request, regulacion_id):
    regulacion = get_object_or_404(Regulacion, id=regulacion_id)
    
    html = render_to_string('spdp/regulacion/pdf.html', {'regulacion': regulacion})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=Regulacion_{regulacion.nombre_registro}.pdf'

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')],
        presentational_hints=True
    )

    return response


import io
import base64
import qrcode
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from .models import SPDP_ActaDelegado

@staff_member_required
def rat_pdf(request, delegado_id):
    delegado = get_object_or_404(SPDP_ActaDelegado, id=delegado_id)

    # -----------------------------
    # 🔐 Generar hash único para RAT
    # -----------------------------
    token_hash = get_random_string(length=32)
    delegado.rat_hash = token_hash  # Guardado temporal en objeto

    # -----------------------------
    # 🔳 Generar QR del RAT
    # -----------------------------
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=4,
    )
    qr_data = f"RAT-{delegado.id}-{token_hash}"
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    qr_url = f"data:image/png;base64,{qr_base64}"

    # -----------------------------
    # 🔄 Traer todos los registros de RAT asociados
    # -----------------------------
    rat_registros = SPDP_ActaDelegado.objects.all()
    



    # -----------------------------
    # Renderizar plantilla HTML
    # -----------------------------
    html = render_to_string('spdp/rat/pdf.html', {
        'delegado': delegado,
        'rat_registros': rat_registros,
        'qr_url': qr_url,
        'rat_hash': token_hash,
    })

    # -----------------------------
    # Crear respuesta PDF
    # -----------------------------
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=RAT_{delegado.nombre_delegado}_{delegado.fecha_nombramiento}.pdf'

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')],
        presentational_hints=True
    )

    return response




from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import SCVSFinancialReport

# ----------------------
# Helpers para formato
# ----------------------
def format_decimal(value):
    """Formatea valores numéricos a 2 decimales, 0.00 si None"""
    if value is None:
        return "0.00"
    return f"{value:.2f}"

def format_text(value):
    """Texto vacío si None"""
    return value if value else ""

# ----------------------
# Vista: Datos Generales
# ----------------------
def txt_datos_generales(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)
    lines = [
        f"RUC|{format_text(reporte.ruc)}",
        f"Nombre|{format_text(reporte.company_name)}",
        f"TipoSociedad|{format_text(reporte.company_type)}",
        f"AñoFiscal|{format_text(reporte.fiscal_year)}",
        f"ActividadEconomica|{format_text(reporte.economic_activity)}",
        f"Moneda|{format_text(reporte.currency)}",
    ]
    content = "\n".join(lines)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{reporte.ruc}_DatosGenerales.txt"'
    return response

# ----------------------
# Vista: Balance General
# ----------------------
def txt_balance_general(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)
    lines = [
        f"EfectivoEquivalentes|{format_decimal(reporte.cash_and_equivalents)}",
        f"InversionesCortoPlazo|{format_decimal(reporte.short_term_investments)}",
        f"CuentasPorCobrar|{format_decimal(reporte.accounts_receivable)}",
        f"Inventarios|{format_decimal(reporte.inventories)}",
        f"OtrosActivosCorrientes|{format_decimal(reporte.other_current_assets)}",
        f"PropiedadPlantaEquipo|{format_decimal(reporte.property_plant_equipment)}",
        f"DepreciacionAcumulada|{format_decimal(reporte.accumulated_depreciation)}",
        f"ActivosIntangibles|{format_decimal(reporte.intangible_assets)}",
        f"OtrosActivosNoCorrientes|{format_decimal(reporte.other_non_current_assets)}",
        f"CuentasPorPagar|{format_decimal(reporte.accounts_payable)}",
        f"PrestamosCortoPlazo|{format_decimal(reporte.short_term_loans)}",
        f"ObligacionesTributarias|{format_decimal(reporte.tax_payables)}",
        f"ObligacionesLaborales|{format_decimal(reporte.labor_obligations)}",
        f"OtrosPasivosCorrientes|{format_decimal(reporte.other_current_liabilities)}",
        f"PrestamosLargoPlazo|{format_decimal(reporte.long_term_loans)}",
        f"Provisiones|{format_decimal(reporte.provisions)}",
        f"OtrosPasivosNoCorrientes|{format_decimal(reporte.other_non_current_liabilities)}",
        f"CapitalSocial|{format_decimal(reporte.share_capital)}",
        f"ReservaLegal|{format_decimal(reporte.legal_reserve)}",
        f"ResultadosAcumulados|{format_decimal(reporte.retained_earnings)}",
        f"ResultadoNeto|{format_decimal(reporte.net_income)}",
    ]
    content = "\n".join(lines)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{reporte.ruc}_BalanceGeneral.txt"'
    return response

# ----------------------
# Vista: Estado de Resultados
# ----------------------
def txt_estado_resultados(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)
    lines = [
        f"IngresosOperativos|{format_decimal(reporte.operating_revenue)}",
        f"CostoVentas|{format_decimal(reporte.cost_of_sales)}",
        f"UtilidadBruta|{format_decimal(reporte.gross_profit)}",
        f"GastosAdministrativos|{format_decimal(reporte.administrative_expenses)}",
        f"GastosVentas|{format_decimal(reporte.selling_expenses)}",
        f"GastosFinancieros|{format_decimal(reporte.financial_expenses)}",
        f"OtrosIngresos|{format_decimal(reporte.other_income)}",
        f"OtrosGastos|{format_decimal(reporte.other_expenses)}",
        f"ImpuestoRenta|{format_decimal(reporte.income_tax)}",
    ]
    content = "\n".join(lines)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{reporte.ruc}_EstadoResultados.txt"'
    return response

# ----------------------
# Vista: Cambios en el Patrimonio
# ----------------------
def txt_cambios_patrimonio(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)
    lines = [
        f"SaldoInicialPatrimonio|{format_decimal(reporte.equity_opening_balance)}",
        f"IncrementosPatrimonio|{format_decimal(reporte.equity_increases)}",
        f"DisminucionesPatrimonio|{format_decimal(reporte.equity_decreases)}",
        f"SaldoFinalPatrimonio|{format_decimal(reporte.equity_closing_balance)}",
    ]
    content = "\n".join(lines)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{reporte.ruc}_CambiosPatrimonio.txt"'
    return response

# ----------------------
# Vista: Flujo de Efectivo y Anexos
# ----------------------
def txt_flujo_anexos(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)
    lines = [
        f"FlujoOperacion|{format_decimal(reporte.cashflow_operating)}",
        f"FlujoInversion|{format_decimal(reporte.cashflow_investing)}",
        f"FlujoFinanciamiento|{format_decimal(reporte.cashflow_financing)}",
        f"FlujoNeto|{format_decimal(reporte.net_cash_flow)}",
        f"CuentasPorCobrarRelacionadas|{format_decimal(reporte.accounts_receivable_related)}",
        f"CuentasPorPagarRelacionadas|{format_decimal(reporte.accounts_payable_related)}",
        f"CostoActivosFijos|{format_decimal(reporte.fixed_assets_cost)}",
        f"DepreciacionActivosFijos|{format_decimal(reporte.fixed_assets_depreciation)}",
        f"ObligacionesFinancieras|{format_decimal(reporte.financial_obligations_total)}",
        f"ParticipacionEmpleados|{format_decimal(reporte.employee_profit_sharing)}",
    ]
    content = "\n".join(lines)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{reporte.ruc}_FlujoEfectivo_Anexos.txt"'
    return response


@staff_member_required
def pdf_datos_generales(request, pk):
    """
    Genera PDF de Datos Generales del reporte SCVSFinancialReport
    """
    # Obtener el reporte
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)

    # ----------------------------
    # Generar QR basado en RUC + Año fiscal
    # ----------------------------
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
    qr_data = f"SCVS-DATOS-{reporte.ruc}-{reporte.fiscal_year}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    qr_url = f"data:image/png;base64,{qr_base64}"

    # ----------------------------
    # Renderizar plantilla HTML
    # ----------------------------
    html = render_to_string('scvs/pdf_datos_generales.html', {
        'reporte': reporte,
        'qr_url': qr_url,
    })

    # ----------------------------
    # Crear respuesta PDF
    # ----------------------------
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="DatosGenerales_{reporte.ruc}_{reporte.fiscal_year}.pdf"'

    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')],
        presentational_hints=True
    )

    return response


@staff_member_required
def pdf_balance(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)

    # QR opcional
    import io, base64, qrcode
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
    qr_data = f"SCVS-BALANCE-{reporte.ruc}-{reporte.fiscal_year}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    qr_url = f"data:image/png;base64,{qr_base64}"

    # Renderizar plantilla HTML
    from django.template.loader import render_to_string
    html = render_to_string('scvs/pdf_balance.html', {'reporte': reporte, 'qr_url': qr_url})

    # Crear PDF
    import weasyprint
    from django.http import HttpResponse
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Balance_{reporte.ruc}_{reporte.fiscal_year}.pdf"'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response, stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')], presentational_hints=True
    )
    return response



@staff_member_required
def pdf_estado_resultados(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
    qr_data = f"SCVS-ESTADORESULTADOS-{reporte.ruc}-{reporte.fiscal_year}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    html = render_to_string('scvs/pdf_estado_resultados.html', {'reporte': reporte, 'qr_url': qr_url})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="EstadoResultados_{reporte.ruc}_{reporte.fiscal_year}.pdf"'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response, stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')], presentational_hints=True
    )
    return response


@staff_member_required
def pdf_cambios_patrimonio(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
    qr_data = f"SCVS-CAMBIOSPATRIMONIO-{reporte.ruc}-{reporte.fiscal_year}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    html = render_to_string('scvs/pdf_cambios_patrimonio.html', {'reporte': reporte, 'qr_url': qr_url})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="CambiosPatrimonio_{reporte.ruc}_{reporte.fiscal_year}.pdf"'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response, stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')], presentational_hints=True
    )
    return response


@staff_member_required
def pdf_flujo_efectivo(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
    qr_data = f"SCVS-FLUJOEFECTIVO-{reporte.ruc}-{reporte.fiscal_year}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    html = render_to_string('scvs/pdf_flujo_efectivo.html', {'reporte': reporte, 'qr_url': qr_url})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="FlujoEfectivo_{reporte.ruc}_{reporte.fiscal_year}.pdf"'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response, stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')], presentational_hints=True
    )
    return response





@staff_member_required
def pdf_anexos(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
    qr_data = f"SCVS-ANEXOS-{reporte.ruc}-{reporte.fiscal_year}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    html = render_to_string('scvs/pdf_anexos.html', {'reporte': reporte, 'qr_url': qr_url})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Anexos_{reporte.ruc}_{reporte.fiscal_year}.pdf"'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response, stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')], presentational_hints=True
    )
    return response



@staff_member_required
def pdf_acta_junta(request, pk):
    acta = get_object_or_404(SCVS_ActasAsamblea, pk=pk)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
    qr_data = f"SCVS-ACTA-{acta.ejercicio_fiscal}-{acta.fecha_asamblea}"
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    html = render_to_string(
        'scvs/pdf_acta_junta.html',
        {'acta': acta, 'qr_url': qr_url}
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="ActaJunta_{acta.ejercicio_fiscal}.pdf"'
    )

    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')],
        presentational_hints=True
    )
    return response


@staff_member_required
def pdf_nomina_socios(request, pk):
    acta = get_object_or_404(SCVS_ActasAsamblea, pk=pk)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
    qr_data = f"SCVS-SOCIOS-{acta.socios_anio_fiscal}"
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    html = render_to_string(
        'scvs/pdf_nomina_socios.html',
        {'acta': acta, 'qr_url': qr_url}
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="NominaSocios_{acta.socios_anio_fiscal}.pdf"'
    )

    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')],
        presentational_hints=True
    )
    return response


@staff_member_required
def pdf_nomina_administradores(request, pk):
    acta = get_object_or_404(SCVS_ActasAsamblea, pk=pk)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
    qr_data = f"SCVS-ADMINS-{acta.admins_anio_fiscal}"
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    html = render_to_string(
        'scvs/pdf_nomina_administradores.html',
        {'acta': acta, 'qr_url': qr_url}
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="NominaAdministradores_{acta.admins_anio_fiscal}.pdf"'
    )

    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')],
        presentational_hints=True
    )
    return response


@staff_member_required
def pdf_informe_gerente(request, pk):
    acta = get_object_or_404(SCVS_ActasAsamblea, pk=pk)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
    qr_data = f"SCVS-GERENTE-{acta.gerente_anio_fiscal}"
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    html = render_to_string(
        'scvs/pdf_informe_gerente.html',
        {'acta': acta, 'qr_url': qr_url}
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="InformeGerente_{acta.gerente_anio_fiscal}.pdf"'
    )

    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')],
        presentational_hints=True
    )
    return response


@staff_member_required
def pdf_scvs_consolidado(request, pk):
    acta = get_object_or_404(SCVS_ActasAsamblea, pk=pk)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
    qr_data = f"SCVS-CONSOLIDADO-{acta.ejercicio_fiscal}"
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    html = render_to_string(
        'scvs/pdf_consolidado.html',
        {'acta': acta, 'qr_url': qr_url}
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="SCVS_Consolidado_{acta.ejercicio_fiscal}.pdf"'
    )

    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')],
        presentational_hints=True
    )
    return response





# views.py
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import SRI_AnexosTributarios
import xml.etree.ElementTree as ET



# ==================================================
# Helper: Función para crear respuesta XML
# ==================================================
def generar_respuesta_xml(xml_tree, filename="anexo.xml"):
    xml_data = ET.tostring(xml_tree, encoding="UTF-8", xml_declaration=True)
    response = HttpResponse(xml_data, content_type="application/xml")
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response




def xml_ats(request, ruc, ejercicio, mes):
    anexo = get_object_or_404(
        SRI_AnexosTributarios,
        ruc=ruc,
        ejercicio_fiscal=ejercicio,
        mes=mes
    )

    def d(value):
        """Convierte a Decimal seguro"""
        return Decimal(value or 0).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    root = ET.Element("iva")

    # =========================
    # CABECERA
    # =========================
    ET.SubElement(root, "TipoIDInformante").text = "R"
    ET.SubElement(root, "IdInformante").text = anexo.ruc
    ET.SubElement(root, "razonSocial").text = anexo.razon_social or ""
    ET.SubElement(root, "Anio").text = str(anexo.ejercicio_fiscal)
    ET.SubElement(root, "Mes").text = f"{int(anexo.mes):02d}"
    ET.SubElement(root, "numEstabRuc").text = "001"

    # =========================
    # CÁLCULO DE MONTOS
    # =========================
    base_no_gravada = d(0)
    base_imponible = d(0)
    base_gravada = d(anexo.ventas_base_iva)
    monto_iva = (base_gravada * Decimal("0.12")).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    monto_ice = d(0)

    total_ventas = (
        base_no_gravada +
        base_imponible +
        base_gravada +
        monto_iva +
        monto_ice
    )

    ET.SubElement(root, "totalVentas").text = f"{total_ventas:.2f}"
    ET.SubElement(root, "codigoOperativo").text = "IVA"

    # =========================
    # COMPRAS (VACÍO PERO OBLIGATORIO)
    # =========================
    ET.SubElement(root, "compras")

    # =========================
    # VENTAS
    # =========================
    ventas = ET.SubElement(root, "ventas")

    # Solo crear detalle si hay ventas
    if total_ventas > 0:

        detalle = ET.SubElement(ventas, "detalleVentas")

        ET.SubElement(detalle, "tpIdCliente").text = anexo.ventas_tipo_id_cliente or "06"
        ET.SubElement(detalle, "idCliente").text = anexo.ventas_id_cliente or "9999999999999"
        ET.SubElement(detalle, "parteRelVtas").text = "NO"
        ET.SubElement(detalle, "tipoComprobante").text = "18"
        ET.SubElement(detalle, "tipoEmision").text = "E"
        ET.SubElement(detalle, "numeroComprobantes").text = "1"

        ET.SubElement(detalle, "baseNoGraIva").text = f"{base_no_gravada:.2f}"
        ET.SubElement(detalle, "baseImponible").text = f"{base_imponible:.2f}"
        ET.SubElement(detalle, "baseImpGrav").text = f"{base_gravada:.2f}"
        ET.SubElement(detalle, "montoIva").text = f"{monto_iva:.2f}"
        ET.SubElement(detalle, "montoIce").text = f"{monto_ice:.2f}"
        ET.SubElement(detalle, "valorRetIva").text = "0.00"
        ET.SubElement(detalle, "valorRetRenta").text = "0.00"

        # =========================
        # FORMAS DE PAGO (OBLIGATORIO)
        # =========================
        forma_pago_codigo = anexo.ventas_forma_cobro or "20"
        formas_pago = ET.SubElement(detalle, "formasDePago")
        ET.SubElement(formas_pago, "formaPago").text = forma_pago_codigo

    # =========================
    # VENTAS POR ESTABLECIMIENTO
    # =========================
    ventas_est = ET.SubElement(root, "ventasEstablecimiento")
    det_est = ET.SubElement(ventas_est, "ventaEst")

    ET.SubElement(det_est, "codEstab").text = "001"
    ET.SubElement(det_est, "ventasEstab").text = f"{total_ventas:.2f}"
    ET.SubElement(det_est, "ivaComp").text = "0.00"

    return generar_respuesta_xml(
        root,
        filename=f"ATS_{anexo.ruc}_{anexo.ejercicio_fiscal}_{int(anexo.mes):02d}.xml"
    )


# ==================================================
# 2. XML RDEP (Relación de Dependencia)
# ==================================================
def xml_rdep(request, ruc, ejercicio, mes):
    anexo = get_object_or_404(SRI_AnexosTributarios, ruc=ruc, ejercicio_fiscal=ejercicio, mes=mes)
    
    root = ET.Element("rdep", attrib={"id": "rdep", "version": "1.0.0"})
    contribuyente = ET.SubElement(root, "contribuyente")
    ET.SubElement(contribuyente, "ruc").text = anexo.ruc
    ET.SubElement(contribuyente, "razonSocial").text = anexo.razon_social
    ET.SubElement(contribuyente, "anio").text = str(anexo.ejercicio_fiscal)
    ET.SubElement(contribuyente, "mes").text = f"{anexo.mes:02d}"
    
    # Empleados
    empleados = ET.SubElement(root, "empleados")
    if anexo.tiene_empleados:
        empleado = ET.SubElement(empleados, "empleado")
        ET.SubElement(empleado, "identificacion").text = anexo.empleado_identificacion or ""
        ET.SubElement(empleado, "nombres").text = anexo.empleado_nombres or ""
        ET.SubElement(empleado, "cargo").text = anexo.empleado_cargo or ""
        ET.SubElement(empleado, "sueldoAnual").text = str(anexo.empleado_sueldo_anual or 0)
        ET.SubElement(empleado, "aporteIESS").text = str(anexo.empleado_aporte_iess or 0)
        ET.SubElement(empleado, "irRetenido").text = str(anexo.empleado_ir_retenido or 0)
    
    return generar_respuesta_xml(root, filename=f"RDEP_{anexo.ruc}_{anexo.ejercicio_fiscal}_{anexo.mes:02d}.xml")


# ==================================================
# 3. XML Dividendos
# ==================================================
def xml_dividendos(request, ruc, ejercicio, mes):
    anexo = get_object_or_404(SRI_AnexosTributarios, ruc=ruc, ejercicio_fiscal=ejercicio, mes=mes)
    
    root = ET.Element("dividendos", attrib={"id": "dividendos", "version": "1.0.0"})
    contribuyente = ET.SubElement(root, "contribuyente")
    ET.SubElement(contribuyente, "ruc").text = anexo.ruc
    ET.SubElement(contribuyente, "razonSocial").text = anexo.razon_social
    ET.SubElement(contribuyente, "anio").text = str(anexo.ejercicio_fiscal)
    ET.SubElement(contribuyente, "mes").text = f"{anexo.mes:02d}"
    
    if anexo.distribuyo_dividendos:
        socio = ET.SubElement(root, "socio")
        ET.SubElement(socio, "identificacion").text = anexo.socio_identificacion or ""
        ET.SubElement(socio, "nombre").text = anexo.socio_nombre or ""
        ET.SubElement(socio, "porcentajeParticipacion").text = str(anexo.socio_porcentaje_participacion or 0)
        ET.SubElement(socio, "dividendoPagado").text = str(anexo.dividendo_pagado or 0)
        ET.SubElement(socio, "impuestoDividendos").text = str(anexo.impuesto_dividendo or 0)
    
    return generar_respuesta_xml(root, filename=f"DIV_{anexo.ruc}_{anexo.ejercicio_fiscal}_{anexo.mes:02d}.xml")


# ==================================================
# 4. XML Partes Relacionadas
# ==================================================
def xml_partes_relacionadas(request, ruc, ejercicio, mes):
    anexo = get_object_or_404(SRI_AnexosTributarios, ruc=ruc, ejercicio_fiscal=ejercicio, mes=mes)
    
    root = ET.Element("partesRelacionadas", attrib={"id": "partes", "version": "1.0.0"})
    contribuyente = ET.SubElement(root, "contribuyente")
    ET.SubElement(contribuyente, "ruc").text = anexo.ruc
    ET.SubElement(contribuyente, "razonSocial").text = anexo.razon_social
    ET.SubElement(contribuyente, "anio").text = str(anexo.ejercicio_fiscal)
    ET.SubElement(contribuyente, "mes").text = f"{anexo.mes:02d}"
    
    if anexo.tiene_partes_relacionadas:
        parte = ET.SubElement(root, "parteRelacionada")
        ET.SubElement(parte, "identificacion").text = anexo.parte_relacionada_identificacion or ""
        ET.SubElement(parte, "nombre").text = anexo.parte_relacionada_nombre or ""
        ET.SubElement(parte, "montoOperacion").text = str(anexo.monto_operacion_parte_relacionada or 0)
        ET.SubElement(parte, "tipoOperacion").text = anexo.tipo_operacion or ""
    
    return generar_respuesta_xml(root, filename=f"PR_{anexo.ruc}_{anexo.ejercicio_fiscal}_{anexo.mes:02d}.xml")






import re
import zipfile
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import SRI_AnexosTributarios
import xml.etree.ElementTree as ET

import re
import xml.etree.ElementTree as ET
from .models import SRI_AnexosTributarios  # Ajusta tu modelo si es necesario


# -----------------------
# Funciones auxiliares
# -----------------------
def limpiar_texto(texto):
    """
    Limpia y normaliza texto para XML: mayúsculas, sin caracteres especiales.
    Reemplaza Ñ por N, devuelve 'NA' si está vacío.
    """
    if not texto:
        return "NA"
    texto = texto.upper().replace("Ñ", "N").strip()
    texto = ''.join(c for c in texto if c.isalnum() or c.isspace())
    return " ".join(texto.split())


def map_ubicacion(provincia, canton, parroquia):
    """
    Convierte nombres de ubicación a códigos válidos para SRI.
    Si es None o no existe en el diccionario, devuelve "NA".
    """
    provincia = (provincia or "").upper()
    canton = (canton or "").upper()
    parroquia = (parroquia or "").upper()

    cod_provincia = {
        "PICHINCHA": "201",
        "GUAYAS": "202",
        # Agregar todas las provincias necesarias...
    }.get(provincia, "NA")

    cod_canton = {
        "QUITO": "20115",
        "GUAYAQUIL": "20201",
        # Agregar todos los cantones necesarios...
    }.get(canton, "NA")

    cod_parroquia = {
        "INAQUITO": "2011550",
        "GUAYAS1": "2020101",
        # Agregar todas las parroquias necesarias...
    }.get(parroquia, "NA")

    return cod_provincia, cod_canton, cod_parroquia


def indent(elem, level=0):
    """
    Aplica sangría bonita para el XML.
    """
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level + 1)
        if not elem[-1].tail or not elem[-1].tail.strip():
            elem[-1].tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


# -----------------------
# Función principal
# -----------------------
def generar_xml_beneficiarios(anexo: SRI_AnexosTributarios):
    """
    Genera XML REBEFICS compatible con SRI.
    """
    root = ET.Element("aps")

    # -----------------------
    # INFORMANTE
    # -----------------------
    ruc_str = str(anexo.ruc).zfill(13)

    ET.SubElement(root, "TipoIDInformante").text = "R"
    ET.SubElement(root, "IdInformante").text = ruc_str
    ET.SubElement(root, "TipoSociedad").text = (anexo.tipo_sociedad or "01").zfill(2)
    ET.SubElement(root, "Anio").text = str(anexo.ejercicio_fiscal)
    ET.SubElement(root, "Mes").text = f"{anexo.mes:02d}" if anexo.mes else "00"
    ET.SubElement(root, "PorcentajeAccionarioNoBolsa").text = f"{float(anexo.porcentaje_accionario_no_bolsa or 0):.2f}"
    ET.SubElement(root, "codigoOperativo").text = anexo.codigo_operativo or "APS"
    ET.SubElement(root, "PorcentajeAccionarioBolsa").text = f"{float(anexo.porcentaje_accionario_bolsa or 0):.2f}"
    ET.SubElement(root, "Anticipada").text = "SI" if anexo.anticipada else "NO"
    ET.SubElement(root, "TipoDeclaracion").text = (anexo.tipo_declaracion or "01")[:2]

    # -----------------------
    # ACCIONISTAS
    # -----------------------
    # Solo crear <accionistas> si hay al menos un accionista
    if anexo.socio_identificacion_rebefics:
        accionistas = ET.SubElement(root, "accionistas")
        s = ET.SubElement(accionistas, "accionista")
        ET.SubElement(s, "tipoSujeto").text = (anexo.socio_tipo_sujeto or "01")[:2]
        ET.SubElement(s, "tipoIdentificacion").text = (anexo.socio_tipo_identificacion or "R")[:1]
        ET.SubElement(s, "identificacionInformantePadre").text = ruc_str
        ET.SubElement(s, "numeroIdentificacion").text = anexo.socio_identificacion_rebefics

        # Desglosar nombre completo
        nombres = (anexo.socio_nombre_rebefics or "").split()
        ET.SubElement(s, "primerNombre").text = nombres[0] if len(nombres) > 0 else "NA"
        ET.SubElement(s, "segundoNombre").text = nombres[1] if len(nombres) > 1 else "NA"
        ET.SubElement(s, "primerApellido").text = nombres[2] if len(nombres) > 2 else "NA"
        ET.SubElement(s, "segundoApellido").text = nombres[3] if len(nombres) > 3 else "NA"
        ET.SubElement(s, "nombresRazonSocial").text = "NA"
        ET.SubElement(s, "tipoRegimenFiscal").text = "01"
        ET.SubElement(s, "tipoSociedadExt").text = "NA"
        ET.SubElement(s, "figuraJuridicaExt").text = "NA"
        ET.SubElement(s, "figuraJuridicaOtroExt").text = "NA"
        ET.SubElement(s, "esSociedadPublicaExt").text = "NO"
        ET.SubElement(s, "Menor10porc").text = "NA"
        ET.SubElement(s, "porcentajeAccionarioNoBolsaExt").text = "0.00"
        ET.SubElement(s, "porcentajeAccionarioBolsaExt").text = "0.00"
        ET.SubElement(s, "esBeneficiarioFinal").text = "SI"

        # infoParticipacionAccionaria
        info = ET.SubElement(s, "infoParticipacionAccionaria")
        ET.SubElement(info, "codigoNivel").text = "1"
        ET.SubElement(info, "tipoRelacionadoSociedad").text = "05"
        ET.SubElement(info, "porcentajeParticipacion").text = f"{float(anexo.socio_porcentaje_rebefics or 0):.2f}"
        ET.SubElement(info, "parteRelacionadaInformante").text = "NO"

        # ubicacionResidenciaFiscal
        ubic = ET.SubElement(s, "ubicacionResidenciaFiscal")
        ET.SubElement(ubic, "paisResidenciaFiscal").text = "593"

    # -----------------------
    # BENEFICIARIOS FINALES
    # -----------------------
    # Solo crear <beneficiarios> si hay al menos un beneficiario
    if anexo.bf_identificacion:
        beneficiarios = ET.SubElement(root, "beneficiarios")
        b = ET.SubElement(beneficiarios, "beneficiario")
        ET.SubElement(b, "tipoIdentificacion").text = (anexo.bf_tipo_identificacion or "C")[:1]
        ET.SubElement(b, "numeroIdentificacion").text = anexo.bf_identificacion
        ET.SubElement(b, "primerNombre").text = anexo.bf_primer_nombre or "NA"
        ET.SubElement(b, "segundoNombre").text = anexo.bf_segundo_nombre or "NA"
        ET.SubElement(b, "primerApellido").text = anexo.bf_primer_apellido or "NA"
        ET.SubElement(b, "segundoApellido").text = anexo.bf_segundo_apellido or "NA"
        ET.SubElement(b, "fechaNacimiento").text = "01/01/1900"
        ET.SubElement(b, "porPropiedad").text = "NO"
        ET.SubElement(b, "porcentajePropiedad").text = "0.00"
        ET.SubElement(b, "porOtrosMotivos").text = "09"
        ET.SubElement(b, "porOtrosRelacionados").text = "NA"
        ET.SubElement(b, "porAdministracion").text = "SI"
        ET.SubElement(b, "nacionalidadUno").text = "593"
        ET.SubElement(b, "nacionalidadDos").text = "NA"
        ET.SubElement(b, "nacionalidadTres").text = "NA"
        ET.SubElement(b, "residenciaFiscal").text = anexo.bf_residencia_fiscal or "593"
        ET.SubElement(b, "jurisdiccion").text = "NA"

        # Mapeo de ubicación a códigos válidos
        prov, cant, parr = map_ubicacion(anexo.bf_provincia, anexo.bf_canton, anexo.bf_parroquia)
        ET.SubElement(b, "provincia").text = anexo.bf_provincia or "01"
        ET.SubElement(b, "ciudad").text = anexo.bf_ciudad or "NA"
        ET.SubElement(b, "canton").text = anexo.bf_canton or "01"
        ET.SubElement(b, "parroquia").text = anexo.bf_parroquia or "01"
        ET.SubElement(b, "calle").text = limpiar_texto(anexo.bf_calle)
        ET.SubElement(b, "numero").text = anexo.bf_numero or "SN"
        ET.SubElement(b, "interseccion").text = limpiar_texto(anexo.bf_interseccion)
        ET.SubElement(b, "codigoPostal").text = anexo.bf_codigo_postal or "0000"
        ET.SubElement(b, "referencia").text = limpiar_texto(anexo.bf_referencia)

    # -----------------------
    # Sangría y retorno
    # -----------------------
    indent(root)
    return ET.tostring(root, encoding="UTF-8", xml_declaration=True)



def zip_beneficiarios_finales(request, ruc, ejercicio):
    """
    Genera y descarga el XML en ZIP.
    """
    anexo = get_object_or_404(
        SRI_AnexosTributarios,
        ruc=ruc,
        ejercicio_fiscal=ejercicio
    )

    xml_bytes = generar_xml_beneficiarios(anexo)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(
            f"REBEFICS_{anexo.ruc}_{anexo.ejercicio_fiscal}.xml",
            xml_bytes
        )

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = (
        f'attachment; filename="REBEFICS_{anexo.ruc}_{anexo.ejercicio_fiscal}.zip"'
    )

    return response




import xml.etree.ElementTree as ET
from django.shortcuts import get_object_or_404

# ==================================================
# XML Conciliación Tributaria
# ==================================================
def xml_conciliacion(request, ruc, ejercicio, mes):
    anexo = get_object_or_404(SRI_AnexosTributarios, ruc=ruc, ejercicio_fiscal=ejercicio, mes=mes)
    
    # Nodo raíz
    root = ET.Element("conciliacionTributaria", attrib={"id": "conciliacion", "version": "1.0.0"})
    
    # Información del contribuyente
    contribuyente = ET.SubElement(root, "contribuyente")
    ET.SubElement(contribuyente, "ruc").text = anexo.ruc
    ET.SubElement(contribuyente, "razonSocial").text = anexo.razon_social
    ET.SubElement(contribuyente, "anio").text = str(anexo.ejercicio_fiscal)
    ET.SubElement(contribuyente, "mes").text = f"{anexo.mes:02d}"
    
    # ==================================================
    # Conciliación tributaria
    # ==================================================
    ET.SubElement(root, "utilidadContable").text = str(anexo.utilidad_contable or 0)
    ET.SubElement(root, "gastosNoDeducibles").text = str(anexo.gastos_no_deducibles or 0)
    ET.SubElement(root, "ingresosExentos").text = str(anexo.ingresos_exentos or 0)
    ET.SubElement(root, "baseImponible").text = str(anexo.base_imponible or 0)
    ET.SubElement(root, "impuestoRentaCausado").text = str(anexo.impuesto_renta_causado or 0)
    
    # ==================================================
    # Generar la respuesta XML
    # ==================================================
    return generar_respuesta_xml(
        root, 
        filename=f"CONC_{anexo.ruc}_{anexo.ejercicio_fiscal}_{anexo.mes:02d}.xml"
    )



# Helper para generar ZIP a partir de un HttpResponse de XML
def generar_zip_desde_xml(xml_response, filename_zip):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(xml_response['Content-Disposition'].split('filename="')[1][:-1], xml_response.content)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/zip")
    response['Content-Disposition'] = f'attachment; filename="{filename_zip}"'
    return response



# ----------------------------
# ZIP ATS
# ----------------------------
def zip_ats(request, ruc, ejercicio, mes):
    anexo = get_object_or_404(SRI_AnexosTributarios, ruc=ruc, ejercicio_fiscal=ejercicio, mes=mes)
    xml_resp = xml_ats(request, ruc, ejercicio, mes)
    filename_zip = f"ATS_{ruc}_{ejercicio}_{mes:02d}.zip"
    return generar_zip_desde_xml(xml_resp, filename_zip)

# ----------------------------
# ZIP RDEP
# ----------------------------
def zip_rdep(request, ruc, ejercicio, mes):
    anexo = get_object_or_404(SRI_AnexosTributarios, ruc=ruc, ejercicio_fiscal=ejercicio, mes=mes)
    xml_resp = xml_rdep(request, ruc, ejercicio, mes)
    filename_zip = f"RDEP_{ruc}_{ejercicio}_{mes:02d}.zip"
    return generar_zip_desde_xml(xml_resp, filename_zip)

# ----------------------------
# ZIP Dividendos
# ----------------------------
def zip_dividendos(request, ruc, ejercicio, mes):
    anexo = get_object_or_404(SRI_AnexosTributarios, ruc=ruc, ejercicio_fiscal=ejercicio, mes=mes)
    xml_resp = xml_dividendos(request, ruc, ejercicio, mes)
    filename_zip = f"DIV_{ruc}_{ejercicio}_{mes:02d}.zip"
    return generar_zip_desde_xml(xml_resp, filename_zip)

# ----------------------------
# ZIP Partes Relacionadas
# ----------------------------
def zip_partes_relacionadas(request, ruc, ejercicio, mes):
    anexo = get_object_or_404(SRI_AnexosTributarios, ruc=ruc, ejercicio_fiscal=ejercicio, mes=mes)
    xml_resp = xml_partes_relacionadas(request, ruc, ejercicio, mes)
    filename_zip = f"PR_{ruc}_{ejercicio}_{mes:02d}.zip"
    return generar_zip_desde_xml(xml_resp, filename_zip)

# ----------------------------
# ZIP Conciliación Tributaria
# ----------------------------
def zip_conciliacion(request, ruc, ejercicio, mes):
    anexo = get_object_or_404(SRI_AnexosTributarios, ruc=ruc, ejercicio_fiscal=ejercicio, mes=mes)
    xml_resp = xml_conciliacion(request, ruc, ejercicio, mes)
    filename_zip = f"CONC_{ruc}_{ejercicio}_{mes:02d}.zip"
    return generar_zip_desde_xml(xml_resp, filename_zip)



# views.py
import io
import zipfile
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import SRI_AnexosTributarios
from . import views as xml_views  # Para llamar a tus funciones xml_ats, xml_rdep, etc.

def descargar_anexos_zip(request, pk):
    """
    Genera un ZIP con todos los XML de un SRI_AnexosTributarios específico
    y lo envía como respuesta para descarga.
    """
    anexo = get_object_or_404(SRI_AnexosTributarios, pk=pk)

    # Crear un buffer para el ZIP
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        # Listado de funciones XML que quieres incluir
        xml_funciones = [
            ("ATS", xml_views.xml_ats),
            ("RDEP", xml_views.xml_rdep),
            ("DIV", xml_views.xml_dividendos),
            ("PR", xml_views.xml_partes_relacionadas),
            ("CONC", xml_views.xml_conciliacion),
        ]

        for nombre, func in xml_funciones:
            # Generar XML en memoria usando las funciones existentes
            xml_response = func(request, ruc=anexo.ruc, ejercicio=anexo.ejercicio_fiscal, mes=getattr(anexo, 'mes', 0))
            xml_data = xml_response.content  # bytes del XML

            # Nombre del archivo dentro del ZIP
            archivo_nombre = f"{nombre}_{anexo.ruc}_{anexo.ejercicio_fiscal}_{getattr(anexo, 'mes', 0):02d}.xml"
            zip_file.writestr(archivo_nombre, xml_data)

    # Preparar respuesta HTTP con el ZIP
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type="application/zip")
    response['Content-Disposition'] = f'attachment; filename="Anexos_{anexo.ruc}_{anexo.ejercicio_fiscal}.zip"'
    return response




# views.py
import io
import base64
import qrcode
import weasyprint

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required

from .models import ContratoLaboral


@staff_member_required
def pdf_contrato_laboral(request, pk):
    contrato = get_object_or_404(ContratoLaboral, pk=pk)

    # ---------------------------
    # Generación QR de certificación
    # ---------------------------
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=4
    )

    qr_data = (
        f"CONTRATO-LABORAL|"
        f"{contrato.empleador_ruc}|"
        f"{contrato.trabajador_identificacion}|"
        f"{contrato.fecha_inicio}|"
        f"{contrato.hash_contrato}"
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    qr_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    # ---------------------------
    # Render HTML
    # ---------------------------
    html = render_to_string(
        "laboral/pdf_contrato_laboral.html",
        {
            "contrato": contrato,
            "qr_url": qr_url,
        }
    )

    # ---------------------------
    # Respuesta PDF
    # ---------------------------
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="Contrato_Laboral_{contrato.trabajador_identificacion}.pdf"'
    )

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS("smartbusinesslaw/static/css/pdf.css")
        ],
        presentational_hints=True
    )

    return response



import io
import base64
import qrcode
import weasyprint

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required

from .models import Nomina


@staff_member_required
def pdf_rol_pagos(request, pk):
    nomina = get_object_or_404(Nomina, pk=pk)

    # ==============================
    # GENERAR QR
    # ==============================
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=4
    )

    qr_data = (
        f"ROL-PAGOS | {nomina.contrato} | "
        f"{nomina.mes}/{nomina.anio} | {nomina.sueldo_a_pagar} | "
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    qr_url = (
        f"data:image/png;base64,"
        f"{base64.b64encode(buffer.getvalue()).decode()}"
    )

    # ==============================
    # RENDER HTML
    # ==============================
    html = render_to_string(
        "nomina/pdf_rol_pagos.html",
        {
            "nomina": nomina,
            "qr_url": qr_url,
        }
    )

    # ==============================
    # RESPONSE PDF
    # ==============================
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="RolPagos_'
        f'{nomina.contrato}_{nomina.mes}_{nomina.anio}.pdf"'
    )

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS(
                "smartbusinesslaw/static/css/pdf.css"
            )
        ],
        presentational_hints=True
    )

    return response



import io
import base64
import qrcode
import weasyprint

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required

from .models import Nomina


@staff_member_required
def pdf_cheque_sueldo(request, pk):
    nomina = get_object_or_404(Nomina, pk=pk)

    # ==============================
    # GENERAR QR
    # ==============================
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=2
    )

    qr_data = (
        f"CHEQUE-SUELDO | "
        f"{nomina.cedula_empleado} | "
        f"{nomina.mes}/{nomina.anio} | "
        f"{nomina.sueldo_a_pagar}"
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    qr_url = (
        f"data:image/png;base64,"
        f"{base64.b64encode(buffer.getvalue()).decode()}"
    )

    # ==============================
    # RENDER HTML
    # ==============================
    html = render_to_string(
        "nomina/pdf_cheque_sueldo.html",
        {
            "nomina": nomina,
            "qr_url": qr_url,
        }
    )

    # ==============================
    # RESPONSE PDF
    # ==============================
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="ChequeSueldo_'
        f'{nomina.apellidos}_{nomina.mes}_{nomina.anio}.pdf"'
    )

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS("static/css/pdf_cheque.css")
        ],
        presentational_hints=True
    )

    return response

