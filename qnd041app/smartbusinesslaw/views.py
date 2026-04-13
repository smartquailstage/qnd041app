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
from .models import SCVSFinancialReport,SCVS_ESF,SCVS_EIR,SCVS_EFE,SCVS_ECP

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
    response['Content-Disposition'] = f'attachment; filename="notas_niif_{reporte.fical_year}.txt"'
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
    # Obtener ESF de forma segura (OneToOne reverse)
    # OneToOne reverse seguro
    try:
        esf = reporte.esf
    except AttributeError:
        return HttpResponse(
            "No existe ESF asociado a este reporte.",
            content_type="text/plain",
            status=404
        )



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

    campos_modelo = esf._meta.fields

    for codigo in codigos:
        valor = None

        for field in campos_modelo:
            if field.name.startswith(f"c_{codigo}"):
                valor = getattr(esf, field.name, None)
                break

        lines.append(f"{codigo} {format_decimal(valor or 0)}")

    content = "\n".join(lines)

    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = (
        'attachment; filename="estado_situacion_financiera_esf.txt"'
    )

    return response


# ----------------------
# Vista: Estado de Resultados
# ----------------------
def txt_estado_resultados(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)
    try:
        eir = reporte.eir
    except AttributeError:
        return HttpResponse(
            "No existe EIR asociado a este reporte.",
            content_type="text/plain",
            status=404
        )

    codigos = [
        "401",
        "40101",
        "40102",
        "4010201",
        "4010202",
        "4010203",
        "4010204",
        "40103",
        "40104",
        "40105",
        "40106",
        "4010601",
        "4010602",
        "4010603",
        "40107",
        "40108",
        "40109",
        "4010901",
        "401090101",
        "401090103",
        "401090104",
        "401090105",
        "401090106",
        "4010902",
        "401090201",
        "401090202",
        "401090203",
        "401090204",
        "401090205",
        "401090206",
        "401090207",
        "401090208",
        "4010903",
        "401090301",
        "401090302",
        "401090303",
        "401090304",
        "40110",
        "4011001",
        "4011002",
        "4011003",
        "4011004",
        "4011005",
        "4011006",
        "40112",
        "40113",
        "40114",
        "40115",
        "40116",
        "402",
        "403",
        "40301",
        "40302",
        "40303",
        "501",
        "50101",
        "5010101",
        "5010102",
        "5010103",
        "5010104",
        "5010105",
        "5010106",
        "5010107",
        "5010108",
        "5010109",
        "5010110",
        "5010111",
        "5010112",
        "50102",
        "5010201",
        "5010202",
        "50103",
        "5010301",
        "5010302",
        "50104",
        "5010401",
        "5010402",
        "5010403",
        "5010404",
        "5010405",
        "5010406",
        "5010407",
        "5010408",
        "50105",
        "5010501",
        "502",
        "50201",
        "5020101",
        "5020102",
        "5020103",
        "5020104",
        "5020105",
        "5020106",
        "5020107",
        "5020108",
        "5020109",
        "5020110",
        "5020111",
        "5020112",
        "5020113",
        "5020114",
        "5020115",
        "5020116",
        "5020117",
        "5020118",
        "5020119",
        "5020120",
        "502012001",
        "502012002",
        "502012003",
        "5020121",
        "502012101",
        "502012102",
        "5020122",
        "502012201",
        "502012202",
        "502012203",
        "502012204",
        "502012205",
        "502012206",
        "502012207",
        "5020123",
        "502012301",
        "502012302",
        "502012303",
        "5020124",
        "5020125",
        "5020126",
        "5020127",
        "5020128",
        "50202",
        "5020201",
        "5020202",
        "5020203",
        "5020204",
        "5020205",
        "5020206",
        "5020207",
        "5020208",
        "5020209",
        "5020210",
        "5020211",
        "5020212",
        "5020213",
        "5020214",
        "5020215",
        "5020216",
        "5020217",
        "5020218",
        "5020219",
        "5020220",
        "5020221",
        "502022101",
        "502022102",
        "502022103",
        "5020222",
        "502022201",
        "502022202",
        "5020223",
        "502022301",
        "502022302",
        "502022303",
        "502022304",
        "502022305",
        "502022306",
        "502022307",
        "5020224",
        "502022401",
        "502022402",
        "502022403",
        "5020225",
        "5020226",
        "5020227",
        "5020228",
        "5020229",
        "50203",
        "5020301",
        "502030101",
        "502030102",
        "502030103",
        "502030104",
        "5020302",
        "502030201",
        "50203020101",
        "50203020103",
        "50203020104",
        "50203020105",
        "50203020106",
        "5020303",
        "502030301",
        "502030302",
        "502030303",
        "502030304",
        "502030305",
        "502030306",
        "502030307",
        "502030308",
        "5020304",
        "502030401",
        "502030402",
        "502030403",
        "502030404",
        "5020305",
        "502030501",
        "502030502",
        "502030503",
        "502030504",
        "5020306",
        "5020307",
        "5020308",
        "5020309",
        "5020310",
        "5020311",
        "5020312",
        "50204",
        "5020401",
        "5020402",
        "600",
        "601",
        "602",
        "603",
        "604",
        "605",
        "606",
        "607",
        "700",
        "701",
        "702",
        "703",
        "704",
        "705",
        "706",
        "707",
        "800",
        "80001",
        "80002",
        "80003",
        "80004",
        "80005",
        "80006",
        "80007",
        "80008",
        "80009",
        "801",
        "80101",
        "80102"
    ]

    lines = []

    # mapa de campos del modelo (una sola vez)
    campos_modelo = eir._meta.fields

    for codigo in codigos:
        valor = None

        for field in campos_modelo:
            if field.name.startswith(f"c_{codigo}"):
                valor = getattr(eir, field.name)
                break

        lines.append(f"{codigo} {format_decimal(valor)}")

    content = "\n".join(lines)

    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = (
        f'attachment; filename="estado_integral_resultados(eir).txt"'
    )

    return response


# ----------------------
# Vista: Flujo de Efectivo y Anexos
# ----------------------
def txt_flujo_anexos(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)
    try:
        efe = reporte.efe
    except AttributeError:
        return HttpResponse(
            "No existe EFE asociado a este reporte.",
            content_type="text/plain",
            status=404
        )


    codigos = [
        "95",
        "9501",
        "950101",
        "95010101",
        "95010102",
        "95010103",
        "95010104",
        "95010105",
        "950102",
        "95010201",
        "95010202",
        "95010203",
        "95010204",
        "95010205",
        "950103",
        "950104",
        "950105",
        "950106",
        "950107",
        "950108",
        "9502",
        "950201",
        "950202",
        "950203",
        "950204",
        "950205",
        "950206",
        "950207",
        "950208",
        "950209",
        "950210",
        "950211",
        "950212",
        "950213",
        "950214",
        "950215",
        "950216",
        "950217",
        "950218",
        "950219",
        "950220",
        "950221",
        "9503",
        "950301",
        "950302",
        "950303",
        "950304",
        "950305",
        "950306",
        "950307",
        "950308",
        "950309",
        "950310",
        "9504",
        "950401",
        "9505",
        "9506",
        "9507",
        "96",
        "97",
        "9701",
        "9702",
        "9703",
        "9704",
        "9705",
        "9706",
        "9707",
        "9708",
        "9709",
        "9710",
        "9711",
        "98",
        "9801",
        "9802",
        "9803",
        "9804",
        "9805",
        "9806",
        "9807",
        "9808",
        "9809",
        "9810",
        "9820"
    ]

    lines = []

    campos_modelo = efe._meta.fields

    for codigo in codigos:
        valor = None
        for field in campos_modelo:
            if field.name.startswith(f"c_{codigo}"):
                valor = getattr(efe, field.name, None)
                break

        lines.append(f"{codigo} {format_decimal(valor)}")

    content = "\n".join(lines)

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="estado_flujo_efectivo(efe).txt"'

    return response

# ----------------------
# Vista: Cambios en el Patrimonio
# ----------------------
def txt_cambios_patrimonio(request, pk):
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)
    try:
        ecp = reporte.ecp
    except AttributeError:
        return HttpResponse(
            "No existe ECP asociado a este reporte.",
            content_type="text/plain",
            status=404
        )


    codigos = [
        ("99", "301"),
        ("99", "302"),
        ("99", "303"),
        ("99", "30401"),
        ("99", "30402"),
        ("99", "30501"),
        ("99", "30502"),
        ("99", "30503"),
        ("99", "30504"),
        ("99", "30601"),
        ("99", "30602"),
        ("99", "30603"),
        ("99", "30604"),
        ("99", "30605"),
        ("99", "30606"),
        ("99", "30607"),
        ("99", "30701"),
        ("99", "30702"),
        ("9901", "301"),
        ("9901", "302"),
        ("9901", "303"),
        ("9901", "30401"),
        ("9901", "30402"),
        ("9901", "30501"),
        ("9901", "30502"),
        ("9901", "30503"),
        ("9901", "30504"),
        ("9901", "30601"),
        ("9901", "30602"),
        ("9901", "30603"),
        ("9901", "30604"),
        ("9901", "30605"),
        ("9901", "30606"),
        ("9901", "30607"),
        ("9901", "30701"),
        ("9901", "30702"),
        ("990101", "301"),
        ("990101", "302"),
        ("990101", "303"),
        ("990101", "30401"),
        ("990101", "30402"),
        ("990101", "30501"),
        ("990101", "30502"),
        ("990101", "30503"),
        ("990101", "30504"),
        ("990101", "30601"),
        ("990101", "30602"),
        ("990101", "30603"),
        ("990101", "30604"),
        ("990101", "30605"),
        ("990101", "30606"),
        ("990101", "30607"),
        ("990101", "30701"),
        ("990101", "30702"),
        ("990102", "301"),
        ("990102", "302"),
        ("990102", "303"),
        ("990102", "30401"),
        ("990102", "30402"),
        ("990102", "30501"),
        ("990102", "30502"),
        ("990102", "30503"),
        ("990102", "30504"),
        ("990102", "30601"),
        ("990102", "30602"),
        ("990102", "30603"),
        ("990102", "30604"),
        ("990102", "30605"),
        ("990102", "30606"),
        ("990102", "30607"),
        ("990102", "30701"),
        ("990102", "30702"),
        ("990103", "301"),
        ("990103", "302"),
        ("990103", "303"),
        ("990103", "30401"),
        ("990103", "30402"),
        ("990103", "30501"),
        ("990103", "30502"),
        ("990103", "30503"),
        ("990103", "30504"),
        ("990103", "30601"),
        ("990103", "30602"),
        ("990103", "30603"),
        ("990103", "30604"),
        ("990103", "30605"),
        ("990103", "30606"),
        ("990103", "30607"),
        ("990103", "30701"),
        ("990103", "30702"),
        ("9902", "301"),
        ("9902", "302"),
        ("9902", "303"),
        ("9902", "30401"),
        ("9902", "30402"),
        ("9902", "30501"),
        ("9902", "30502"),
        ("9902", "30503"),
        ("9902", "30504"),
        ("9902", "30601"),
        ("9902", "30602"),
        ("9902", "30603"),
        ("9902", "30604"),
        ("9902", "30605"),
        ("9902", "30606"),
        ("9902", "30607"),
        ("9902", "30701"),
        ("9902", "30702"),
        ("990201", "301"),
        ("990201", "302"),
        ("990201", "303"),
        ("990201", "30401"),
        ("990201", "30402"),
        ("990201", "30501"),
        ("990201", "30502"),
        ("990201", "30503"),
        ("990201", "30504"),
        ("990201", "30601"),
        ("990201", "30602"),
        ("990201", "30603"),
        ("990201", "30604"),
        ("990201", "30605"),
        ("990201", "30606"),
        ("990201", "30607"),
        ("990201", "30701"),
        ("990201", "30702"),
        ("990202", "301"),
        ("990202", "302"),
        ("990202", "303"),
        ("990202", "30401"),
        ("990202", "30402"),
        ("990202", "30501"),
        ("990202", "30502"),
        ("990202", "30503"),
        ("990202", "30504"),
        ("990202", "30601"),
        ("990202", "30602"),
        ("990202", "30603"),
        ("990202", "30604"),
        ("990202", "30605"),
        ("990202", "30606"),
        ("990202", "30607"),
        ("990202", "30701"),
        ("990202", "30702"),
        ("990203", "301"),
        ("990203", "302"),
        ("990203", "303"),
        ("990203", "30401"),
        ("990203", "30402"),
        ("990203", "30501"),
        ("990203", "30502"),
        ("990203", "30503"),
        ("990203", "30504"),
        ("990203", "30601"),
        ("990203", "30602"),
        ("990203", "30603"),
        ("990203", "30604"),
        ("990203", "30605"),
        ("990203", "30606"),
        ("990203", "30607"),
        ("990203", "30701"),
        ("990203", "30702"),
        ("990204", "301"),
        ("990204", "302"),
        ("990204", "303"),
        ("990204", "30401"),
        ("990204", "30402"),
        ("990204", "30501"),
        ("990204", "30502"),
        ("990204", "30503"),
        ("990204", "30504"),
        ("990204", "30601"),
        ("990204", "30602"),
        ("990204", "30603"),
        ("990204", "30604"),
        ("990204", "30605"),
        ("990204", "30606"),
        ("990204", "30607"),
        ("990204", "30701"),
        ("990204", "30702"),
        ("990205", "301"),
        ("990205", "302"),
        ("990205", "303"),
        ("990205", "30401"),
        ("990205", "30402"),
        ("990205", "30501"),
        ("990205", "30502"),
        ("990205", "30503"),
        ("990205", "30504"),
        ("990205", "30601"),
        ("990205", "30602"),
        ("990205", "30603"),
        ("990205", "30604"),
        ("990205", "30605"),
        ("990205", "30606"),
        ("990205", "30607"),
        ("990205", "30701"),
        ("990205", "30702"),
        ("990206", "301"),
        ("990206", "302"),
        ("990206", "303"),
        ("990206", "30401"),
        ("990206", "30402"),
        ("990206", "30501"),
        ("990206", "30502"),
        ("990206", "30503"),
        ("990206", "30504"),
        ("990206", "30601"),
        ("990206", "30602"),
        ("990206", "30603"),
        ("990206", "30604"),
        ("990206", "30605"),
        ("990206", "30606"),
        ("990206", "30607"),
        ("990206", "30701"),
        ("990206", "30702"),
        ("990207", "301"),
        ("990207", "302"),
        ("990207", "303"),
        ("990207", "30401"),
        ("990207", "30402"),
        ("990207", "30501"),
        ("990207", "30502"),
        ("990207", "30503"),
        ("990207", "30504"),
        ("990207", "30601"),
        ("990207", "30602"),
        ("990207", "30603"),
        ("990207", "30604"),
        ("990207", "30605"),
        ("990207", "30606"),
        ("990207", "30607"),
        ("990207", "30701"),
        ("990207", "30702"),
        ("990208", "301"),
        ("990208", "302"),
        ("990208", "303"),
        ("990208", "30401"),
        ("990208", "30402"),
        ("990208", "30501"),
        ("990208", "30502"),
        ("990208", "30503"),
        ("990208", "30504"),
        ("990208", "30601"),
        ("990208", "30602"),
        ("990208", "30603"),
        ("990208", "30604"),
        ("990208", "30605"),
        ("990208", "30606"),
        ("990208", "30607"),
        ("990208", "30701"),
        ("990208", "30702"),
        ("990209", "301"),
        ("990209", "302"),
        ("990209", "303"),
        ("990209", "30401"),
        ("990209", "30402"),
        ("990209", "30501"),
        ("990209", "30502"),
        ("990209", "30503"),
        ("990209", "30504"),
        ("990209", "30601"),
        ("990209", "30602"),
        ("990209", "30603"),
        ("990209", "30604"),
        ("990209", "30605"),
        ("990209", "30606"),
        ("990209", "30607"),
        ("990209", "30701"),
        ("990209", "30702"),
        ("990210", "301"),
        ("990210", "302"),
        ("990210", "303"),
        ("990210", "30401"),
        ("990210", "30402"),
        ("990210", "30501"),
        ("990210", "30502"),
        ("990210", "30503"),
        ("990210", "30504"),
        ("990210", "30601"),
        ("990210", "30602"),
        ("990210", "30603"),
        ("990210", "30604"),
        ("990210", "30605"),
        ("990210", "30606"),
        ("990210", "30607"),
        ("990210", "30701"),
        ("990210", "30702"),
        ("99", "30"),
        ("99", "31"),
        ("9901", "30"),
        ("9901", "31"),
        ("9902", "30"),
        ("9902", "31"),
        ("990101", "30"),
        ("990101", "31"),
        ("990102", "30"),
        ("990102", "31"),
        ("990103", "30"),
        ("990103", "31"),
        ("990201", "30"),
        ("990201", "31"),
        ("990202", "30"),
        ("990202", "31"),
        ("990203", "30"),
        ("990203", "31"),
        ("990204", "30"),
        ("990204", "31"),
        ("990205", "30"),
        ("990205", "31"),
        ("990206", "30"),
        ("990206", "31"),
        ("990207", "30"),
        ("990207", "31"),
        ("990208", "30"),
        ("990208", "31"),
        ("990209", "30"),
        ("990209", "31"),
        ("990210", "30"),
        ("990210", "31")
    ]

    lines = []

    # campos del modelo como lista de nombres
    campos_modelo = [f.name for f in ecp._meta.fields]

    for codigo, subcodigo in codigos:

        valor = None

        # 🔥 construir prefijo correcto
        if subcodigo and subcodigo != "-":
            prefijo = f"c_{codigo}_{subcodigo}"
        else:
            prefijo = f"c_{codigo}"

        # 🔥 buscar campo que coincida EXACTAMENTE o por inicio
        for field_name in campos_modelo:
            if field_name.startswith(prefijo):
                valor = getattr(ecp, field_name)
                break

        # 🔥 asegurar formato seguro
        valor_formateado = format_decimal(valor) if valor is not None else "0.00"

        lines.append(f"{codigo} {subcodigo} {valor_formateado}")

    contenido_txt = "\n".join(lines)

    response = HttpResponse(contenido_txt, content_type="text/plain")
    response["Content-Disposition"] = (
        f'attachment; filename="Cambio_Patrimonio(ecp).txt"'
    )

    return response



@staff_member_required
def pdf_datos_generales(request, pk):
    """
    Genera PDF de Datos Generales del reporte SCVSFinancialReport
    """
    # Obtener el reporte
    reporte = get_object_or_404(SCVSFinancialReport, pk=pk)
    eir = reporte.eir

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
        'eir': eir,

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
