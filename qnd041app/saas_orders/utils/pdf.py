# utils/pdf.py
from django.template.loader import render_to_string
import weasyprint
from io import BytesIO

def generate_order_pdf(order, request):
    html = render_to_string('saas_orders/order/pdf2.html', {'order': order})
    pdf_file = BytesIO()

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        pdf_file,
        stylesheets=[weasyprint.CSS('saas_orders/static/css/pdf.css')],
        presentational_hints=True
    )

    return pdf_file.getvalue()  # devuelve bytes
