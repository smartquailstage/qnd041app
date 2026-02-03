from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from .models import SPDP_ActaDelegado


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

def generar_txt_scvs(request, pk):
    """
    Genera un archivo .txt compatible con la Superintendencia de Compañías
    a partir del registro SCVSFinancialReport identificado por pk.
    """
    # Obtener el reporte
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)

    # Construir contenido del .txt
    lines = []

    # ----------------------
    # Sección: Datos Generales
    # ----------------------
    lines.append(f"RUC|{reporte.ruc}")
    lines.append(f"Nombre|{reporte.company_name}")
    lines.append(f"TipoSociedad|{reporte.company_type}")
    lines.append(f"AñoFiscal|{reporte.fiscal_year}")
    lines.append(f"ActividadEconomica|{reporte.economic_activity}")
    lines.append(f"Moneda|{reporte.currency}")

    # ----------------------
    # Sección: Balance General
    # ----------------------
    lines.append(f"EfectivoEquivalentes|{reporte.cash_and_equivalents}")
    lines.append(f"InversionesCortoPlazo|{reporte.short_term_investments}")
    lines.append(f"CuentasPorCobrar|{reporte.accounts_receivable}")
    lines.append(f"Inventarios|{reporte.inventories}")
    lines.append(f"OtrosActivosCorrientes|{reporte.other_current_assets}")
    lines.append(f"PropiedadPlantaEquipo|{reporte.property_plant_equipment}")
    lines.append(f"DepreciacionAcumulada|{reporte.accumulated_depreciation}")
    lines.append(f"ActivosIntangibles|{reporte.intangible_assets}")
    lines.append(f"OtrosActivosNoCorrientes|{reporte.other_non_current_assets}")
    lines.append(f"CuentasPorPagar|{reporte.accounts_payable}")
    lines.append(f"PrestamosCortoPlazo|{reporte.short_term_loans}")
    lines.append(f"ObligacionesTributarias|{reporte.tax_payables}")
    lines.append(f"ObligacionesLaborales|{reporte.labor_obligations}")
    lines.append(f"OtrosPasivosCorrientes|{reporte.other_current_liabilities}")
    lines.append(f"PrestamosLargoPlazo|{reporte.long_term_loans}")
    lines.append(f"Provisiones|{reporte.provisions}")
    lines.append(f"OtrosPasivosNoCorrientes|{reporte.other_non_current_liabilities}")
    lines.append(f"CapitalSocial|{reporte.share_capital}")
    lines.append(f"ReservaLegal|{reporte.legal_reserve}")
    lines.append(f"ResultadosAcumulados|{reporte.retained_earnings}")
    lines.append(f"ResultadoNeto|{reporte.net_income}")

    # ----------------------
    # Sección: Estado de Resultados
    # ----------------------
    lines.append(f"IngresosOperativos|{reporte.operating_revenue}")
    lines.append(f"CostoVentas|{reporte.cost_of_sales}")
    lines.append(f"UtilidadBruta|{reporte.gross_profit}")
    lines.append(f"GastosAdministrativos|{reporte.administrative_expenses}")
    lines.append(f"GastosVentas|{reporte.selling_expenses}")
    lines.append(f"GastosFinancieros|{reporte.financial_expenses}")
    lines.append(f"OtrosIngresos|{reporte.other_income}")
    lines.append(f"OtrosGastos|{reporte.other_expenses}")
    lines.append(f"ImpuestoRenta|{reporte.income_tax}")

    # ----------------------
    # Sección: Cambios en el Patrimonio
    # ----------------------
    lines.append(f"SaldoInicialPatrimonio|{reporte.equity_opening_balance}")
    lines.append(f"IncrementosPatrimonio|{reporte.equity_increases}")
    lines.append(f"DisminucionesPatrimonio|{reporte.equity_decreases}")
    lines.append(f"SaldoFinalPatrimonio|{reporte.equity_closing_balance}")

    # ----------------------
    # Sección: Flujo de Efectivo
    # ----------------------
    lines.append(f"FlujoOperacion|{reporte.cashflow_operating}")
    lines.append(f"FlujoInversion|{reporte.cashflow_investing}")
    lines.append(f"FlujoFinanciamiento|{reporte.cashflow_financing}")
    lines.append(f"FlujoNeto|{reporte.net_cash_flow}")

    # ----------------------
    # Sección: Anexos SCVS
    # ----------------------
    lines.append(f"CuentasPorCobrarRelacionadas|{reporte.accounts_receivable_related}")
    lines.append(f"CuentasPorPagarRelacionadas|{reporte.accounts_payable_related}")
    lines.append(f"CostoActivosFijos|{reporte.fixed_assets_cost}")
    lines.append(f"DepreciacionActivosFijos|{reporte.fixed_assets_depreciation}")
    lines.append(f"ObligacionesFinancieras|{reporte.financial_obligations_total}")
    lines.append(f"ParticipacionEmpleados|{reporte.employee_profit_sharing}")

    # ----------------------
    # Construir contenido
    # ----------------------
    content = "\n".join(lines)

    # ----------------------
    # Respuesta HTTP para descargar el archivo
    # ----------------------
    response = HttpResponse(content, content_type='text/plain')
    filename = f"{reporte.ruc}_SCVS_{reporte.fiscal_year}.txt"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response
