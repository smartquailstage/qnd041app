from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from .models import SPDP_ActaDelegado
from .models import SCVS_ActasAsamblea, ClausulaContrato


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
from decimal import Decimal, ROUND_HALF_UP
from datetime import date

from .models import CartaNombramiento

@staff_member_required
def carta_nombramiento_pdf(request, carta_id):
    # Obtener la carta
    carta = get_object_or_404(CartaNombramiento, id=carta_id)

        # Generar hash único para incidente si aún no existe
    if not carta.hash_nombramiento:
        carta.hash_nombramiento = get_random_string(32)
        carta.save()

    # Generar QR opcional basado en la ID de la carta
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=4,
    )
    qr_data = f"CARTA-{carta.id}"
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    qr_url = f"data:image/png;base64,{qr_base64}"

    # Renderizar plantilla HTML con los datos de la carta
    html = render_to_string('scvs/pdf_carta_nombramiento.html', {
        'carta': carta,
        'qr_url': qr_url,
    })

    # Crear respuesta PDF con WeasyPrint
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=carta_nombramiento_{carta.id}.pdf'

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('smartbusinesslaw/static/css/pdf.css')],
        presentational_hints=True
    )

    return response



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

def format_decimal(value):
    if value is None:
        return "0.00"
    return f"{value:.2f}"


def txt_balance_general(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)


    codigos = [
        "1",
        "101",
        "10101",
        "1010101",
        "1010102",
        "1010103",
        "10102",
        "1010201",
        "101020101",
        "10102010101",
        "10102010102",
        "10102010103",
        "10102010104",
        "10102010105",
        "10102010106",
        "101020102",
        "10102010201",
        "10102010202",
        "10102010203",
        "10102010204",
        "10102010205",
        "10102010206",
        "10102010207",
        "10102010208",
        "10102010209",
        "10102010210",
        "10102010211",
        "10102010212",
        "10102010213",
        "10102010214",
        "10102010215",
        "10102010216",
        "10102010217",
        "10102010218",
        "10102010219",
        "10102010220",
        "10102010221",
        "10102010222",
        "10102010223",
        "101020103",
        "10102010301",
        "10102010302",
        "10102010303",
        "10102010304",
        "1010202",
        "101020201",
        "10102020101",
        "10102020102",
        "10102020103",
        "10102020104",
        "10102020105",
        "10102020106",
        "101020202",
        "10102020201",
        "10102020202",
        "10102020203",
        "10102020204",
        "10102020205",
        "10102020206",
        "10102020207",
        "10102020208",
        "10102020209",
        "10102020210",
        "10102020211",
        "10102020212",
        "10102020213",
        "10102020214",
        "10102020215",
        "10102020216",
        "10102020217",
        "10102020218",
        "10102020219",
        "10102020220",
        "10102020221",
        "10102020222",
        "10102020223",
        "1010203",
        "101020302",
        "10102030201",
        "10102030202",
        "10102030203",
        "10102030204",
        "10102030205",
        "10102030206",
        "10102030207",
        "10102030208",
        "10102030209",
        "10102030210",
        "10102030211",
        "10102030212",
        "10102030213",
        "10102030214",
        "10102030215",
        "10102030216",
        "10102030217",
        "10102030218",
        "10102030219",
        "10102030220",
        "10102030221",
        "10102030222",
        "10102030223",
        "1010204",
        "101020401",
        "101020402",
        "101020403",
        "1010205",
        "101020501",
        "10102050101",
        "10102050102",
        "101020502",
        "10102050201",
        "10102050202",
        "10102050203",
        "10102050204",
        "10102050207",
        "10102050208",
        "10102050209",
        "10102050210",
        "10102050211",
        "10102050212",
        "10102050213",
        "10102050214",
        "10102050215",
        "10102050216",
        "10102050217",
        "10102050218",
        "10102050219",
        "10102050220",
        "10102050221",
        "1010206",
        "101020601",
        "101020602",
        "101020603",
        "101020604",
        "1010207",
        "10103",
        "1010301",
        "1010302",
        "1010303",
        "1010304",
        "1010305",
        "1010306",
        "1010307",
        "1010308",
        "1010309",
        "1010310",
        "1010311",
        "1010312",
        "1010313",
        "10104",
        "1010401",
        "1010402",
        "1010403",
        "1010404",
        "10105",
        "1010501",
        "1010502",
        "1010503",
        "10106",
        "10107",
        "10108",
        "102",
        "10201",
        "1020101",
        "1020102",
        "1020103",
        "1020104",
        "1020105",
        "1020106",
        "1020107",
        "1020108",
        "1020109",
        "1020110",
        "1020111",
        "1020112",
        "1020113",
        "1020114",
        "102011401",
        "102011402",
        "102011403",
        "10202",
        "1020201",
        "102020101",
        "102020102",
        "1020202",
        "102020201",
        "102020202",
        "1020203",
        "1020204",
        "10203",
        "1020301",
        "1020302",
        "1020303",
        "1020304",
        "1020305",
        "1020306",
        "10204",
        "1020401",
        "1020402",
        "1020403",
        "1020404",
        "1020405",
        "1020406",
        "1020407",
        "10205",
        "10206",
        "1020601",
        "1020602",
        "1020603",
        "1020604",
        "1020605",
        "1020606",
        "10207",
        "1020701",
        "1020702",
        "1020703",
        "10208",
        "1020801",
        "1020802",
        "1020803",
        "1020805",
        "1020806",
        "1020807",
        "1020808",
        "1020809",
        "1020810",
        "1020811",
        "10209",
        "1020901",
        "1020902",
        "1020903",
        "10210",
        "1021001",
        "1021002",
        "1021003",
        "1021004",
        "2",
        "201",
        "20101",
        "20102",
        "20103",
        "2010301",
        "201030101",
        "201030102",
        "201030103",
        "2010302",
        "201030201",
        "201030202",
        "201030203",
        "20104",
        "2010401",
        "2010402",
        "20105",
        "2010501",
        "2010502",
        "20106",
        "2010601",
        "2010602",
        "2010603",
        "2010604",
        "2010605",
        "20107",
        "2010701",
        "2010702",
        "2010703",
        "2010704",
        "2010705",
        "2010706",
        "2010707",
        "20108",
        "2010801",
        "201080101",
        "201080102",
        "201080103",
        "201080104",
        "2010802",
        "201080201",
        "201080202",
        "201080203",
        "201080204",
        "20109",
        "20110",
        "2011001",
        "2011002",
        "20111",
        "20112",
        "2011201",
        "2011202",
        "20113",
        "2011301",
        "2011302",
        "2011303",
        "2011304",
        "2011305",
        "2011306",
        "2011307",
        "2011308",
        "2011309",
        "2011310",
        "2011311",
        "2011312",
        "20114",
        "202",
        "20201",
        "20202",
        "2020201",
        "202020101",
        "202020102",
        "202020103",
        "2020202",
        "202020201",
        "202020202",
        "202020203",
        "20203",
        "2020301",
        "2020302",
        "20204",
        "2020401",
        "202040101",
        "202040102",
        "202040103",
        "202040104",
        "2020402",
        "202040201",
        "202040202",
        "202040203",
        "202040204",
        "20205",
        "2020501",
        "2020502",
        "2020503",
        "2020504",
        "2020505",
        "20206",
        "2020601",
        "2020602",
        "20207",
        "2020701",
        "2020702",
        "20208",
        "20209",
        "2020901",
        "2020902",
        "20210",
        "3",
        "30",
        "301",
        "30101",
        "30102",
        "30103",
        "30104",
        "30105",
        "3010501",
        "3010502",
        "302",
        "303",
        "304",
        "30401",
        "30402",
        "305",
        "30501",
        "30502",
        "30503",
        "30504",
        "306",
        "30601",
        "30602",
        "30603",
        "30604",
        "30605",
        "30606",
        "30607",
        "307",
        "30701",
        "30702",
        "31"
    ]

    lines = []

    campos_modelo = {f.name: f.name for f in reporte._meta.fields}

    for codigo in codigos:
        valor = None
        for field_name in campos_modelo:
            if field_name.startswith(f"c_{codigo}_"):
                valor = getattr(reporte, field_name, None)
                break

        lines.append(f"{codigo} {format_decimal(valor)}")

    content = "\n".join(lines)

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="estado_situacion_{reporte.id}.txt"'

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

from django.db.models.functions import Cast, Substr
from django.db.models import IntegerField

@staff_member_required
def pdf_acta_junta(request, pk):
    acta = get_object_or_404(SCVS_ActasAsamblea, pk=pk)

    # Generar hash único para incidente si aún no existe
    if not acta.acta_hash:
        acta.acta_hash = get_random_string(32)
        acta.save()

    clausulas = acta.clausulas.annotate(
            clausula_num=Cast(
                Substr('clausula', 10),  # Extrae número después de "CLAUSULA_"
                IntegerField()
            )
    ).order_by('clausula_num')

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
        {'acta': acta, 'qr_url': qr_url,"clausulas": clausulas,"acta_hash": acta.acta_hash}
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
        base_gravada).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


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
    if anexo.socio_identificacion:
        accionistas = ET.SubElement(root, "accionistas")
        s = ET.SubElement(accionistas, "accionista")
        ET.SubElement(s, "tipoSujeto").text = (anexo.socio_tipo_sujeto or "01")[:2]
        ET.SubElement(s, "tipoIdentificacion").text = (anexo.socio_tipo_identificacion or "R")[:1]
        ET.SubElement(s, "identificacionInformantePadre").text = ruc_str
        ET.SubElement(s, "numeroIdentificacion").text = anexo.socio_identificacion

        nombres = (anexo.socio_nombre or "").split()
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

        info = ET.SubElement(s, "infoParticipacionAccionaria")
        ET.SubElement(info, "codigoNivel").text = "1"
        ET.SubElement(info, "tipoRelacionadoSociedad").text = "05"
        ET.SubElement(info, "porcentajeParticipacion").text = f"{float(anexo.socio_porcentaje or 0):.2f}"
        ET.SubElement(info, "parteRelacionadaInformante").text = "NO"

        ubic = ET.SubElement(s, "ubicacionResidenciaFiscal")
        ET.SubElement(ubic, "paisResidenciaFiscal").text = "593"

    # -----------------------
    # BENEFICIARIOS FINALES
    # -----------------------
    if anexo.bf_identificacion:
        beneficiarios = ET.SubElement(root, "beneficiarios")
        b = ET.SubElement(beneficiarios, "beneficiario")
        ET.SubElement(b, "tipoIdentificacion").text = (anexo.bf_tipo_identificacion or "C")[:1]
        ET.SubElement(b, "numeroIdentificacion").text = anexo.bf_identificacion
        ET.SubElement(b, "primerNombre").text = anexo.bf_primer_nombre or "NA"
        ET.SubElement(b, "segundoNombre").text = anexo.bf_segundo_nombre or "NA"
        ET.SubElement(b, "primerApellido").text = anexo.bf_primer_apellido or "NA"
        ET.SubElement(b, "segundoApellido").text = anexo.bf_segundo_apellido or "NA"

        fecha_nac = anexo.bf_fecha_nacimiento
        ET.SubElement(b, "fechaNacimiento").text = fecha_nac.strftime("%d/%m/%Y") if fecha_nac else "1900-01-01"

        ET.SubElement(b, "porPropiedad").text = anexo.bf_por_propiedad or "NO"
        ET.SubElement(b, "porcentajePropiedad").text = f"{float(anexo.bf_porcentaje_participacion or 0):.2f}"
        ET.SubElement(b, "porOtrosMotivos").text = anexo.bf_por_otros_motivos or "09"
        ET.SubElement(b, "porOtrosRelacionados").text = "NA"  # <- agregado
        ET.SubElement(b, "porAdministracion").text = anexo.bf_por_administracion or "SI"
        ET.SubElement(b, "nacionalidadUno").text = anexo.bf_nacionalidad_uno or "593"
        ET.SubElement(b, "nacionalidadDos").text = anexo.bf_nacionalidad_dos or "NA"
        ET.SubElement(b, "residenciaFiscal").text = anexo.bf_residencia_fiscal or "593"
        ET.SubElement(b, "jurisdiccion").text = getattr(anexo, "bf_jurisdiccion", "NA")


        ET.SubElement(b, "provincia").text = anexo.bf_provincia or "01"
        ET.SubElement(b, "ciudad").text = anexo.bf_ciudad or "QUITO"
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
