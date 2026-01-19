import io
import base64
import qrcode
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint

from .models import Contrato


@staff_member_required
def admin_contract_pdf(request, contrato_id):
    # ------------------------------
    # Obtener contrato
    # ------------------------------
    contrato = get_object_or_404(Contrato, id=contrato_id)

    # ------------------------------
    # Generar HASH único (si no existe)
    # ------------------------------
    if not contrato.contract_hash:
        import hashlib, uuid
        unique_string = f"{contrato.id}-{uuid.uuid4()}"
        contrato.contract_hash = hashlib.sha256(unique_string.encode("utf-8")).hexdigest()
        contrato.save(update_fields=["contract_hash"])

    # ------------------------------
    # URL de verificación
    # ------------------------------
    verification_url = (
        f"http://ec.smartquail.io/es/business_customer_projects/"
        f"verify/contract/{contrato.contract_hash}/"
    )

    # ------------------------------
    # Generar QR con información del contrato
    # ------------------------------
    qr_data = (
        "SANTIAGO SILVA DOMINGUEZ MAURICIO\n"
        "REPRESENTANTE LEGAL\n"
        "SMARTQUAIL S.A.S\n"
        "R.U.C: 1793206532-001\n"
        "UIO-EC\n"
        f"CONTRATO: {contrato.numero_contrato}\n"
        f"ID TOKEN CONTRACT: {contrato.contract_hash}\n"
      #  f"Validar contrato: {verification_url}"
    )

    qr = qrcode.QRCode(version=1, box_size=1, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    qr_data_url = f"data:image/png;base64,{qr_base64}"

    # ------------------------------
    # Renderizar HTML para PDF
    # ------------------------------
    html = render_to_string(
        "contracts/contrato_pdf.html",  # Plantilla que debes crear
        {
            "contrato": contrato,
            "clausulas": contrato.clausulas.all(),
            "qr_url": qr_data_url,
            "contract_hash": contrato.contract_hash,
           # "verification_url": verification_url,
        }
    )

    # ------------------------------
    # Generar PDF con WeasyPrint
    # ------------------------------
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=contrato_{contrato.id}.pdf"

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[weasyprint.CSS("smartcontracts/static/css/contrato.css")],
        presentational_hints=True
    )

    return response
