from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from io import BytesIO
import weasyprint
from django.conf import settings
from saas_orders.models import SaaSOrder

@shared_task
def send_contracts(order_id):
    # Obtén la orden
    order = SaaSOrder.objects.get(id=order_id)
    domain = "ec.smartquail.io"

    # Evitar errores de Fontconfig
    os.environ['FONTCONFIG_PATH'] = '/tmp/fontconfig'
    os.environ['FONTCONFIG_CACHE'] = '/tmp/fontconfig_cache'
    os.makedirs(os.environ['FONTCONFIG_CACHE'], exist_ok=True)

    # Renderizar el HTML para cada contrato
    ip_contract_html = render_to_string(
        'saas_orders/contracts/contract_ip.html',
        {'order': order, 'domain': domain}
    )

    development_contract_html = render_to_string(
        'saas_orders/contracts/contract_development.html',
        {'order': order, 'domain': domain}
    )

    cloud_contract_html = render_to_string(
        'saas_orders/contracts/contract_cloud_rent.html',
        {'order': order, 'domain': domain}
    )

    # Asunto del correo
    subject = f'Su contrato de compra del software {order.items.first().product.name} está listo'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [order.email]

    # Crear el mensaje de correo electrónico
    html_message = render_to_string(
        'saas_orders/mails/contracts/order_contracts.html',
        {'order': order, 'domain': domain}
    )

    email = EmailMultiAlternatives(
        subject,
        "Su contrato está listo",
        from_email,
        to_email
    )
    email.attach_alternative(html_message, "text/html")

    # ------------------------------
    # 📄 1) Generar PDF de cada contrato
    # ------------------------------
    # Generar PDF para el contrato de propiedad intelectual
    ip_contract_out = BytesIO()
    weasyprint.HTML(string=ip_contract_html, base_url=f"https://{domain}/").write_pdf(
        ip_contract_out,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/contract_ip.css')],
        presentational_hints=True
    )

    # Generar PDF para el contrato de desarrollo
    development_contract_out = BytesIO()
    weasyprint.HTML(string=development_contract_html, base_url=f"https://{domain}/").write_pdf(
        development_contract_out,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/contract_dev.css')],
        presentational_hints=True
    )

    # Generar PDF para el contrato de alquiler de recursos en la nube
    cloud_contract_out = BytesIO()
    weasyprint.HTML(string=cloud_contract_html, base_url=f"https://{domain}/").write_pdf(
        cloud_contract_out,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/contract_resources.css')],
        presentational_hints=True
    )

    # Adjuntar los tres contratos al correo
    email.attach(f"contract_ip_{order.id}.pdf", ip_contract_out.getvalue(), 'application/pdf')
    email.attach(f"contract_development_{order.id}.pdf", development_contract_out.getvalue(), 'application/pdf')
    email.attach(f"contract_cloud_rent_{order.id}.pdf", cloud_contract_out.getvalue(), 'application/pdf')

    # Enviar el correo
    email.send()

    # Marcar email como enviado
    order.contracts_sent = True
    order.save()

    return True
