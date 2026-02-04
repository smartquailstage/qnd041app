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
