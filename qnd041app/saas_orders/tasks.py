from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from .models import SaaSOrder
from .utils.pdf import generate_order_pdf
from django.conf import settings  # Importar configuraciones

@shared_task
def order_created(order_id):
    order = SaaSOrder.objects.get(id=order_id)

    # Tener dominio para generar URLs en templates
    current_site = Site.objects.get_current()
    domain = current_site.domain

    # Renderizar plantilla HTML del correo
    html_message = render_to_string(
        'saas_orders/mails/invoices/order_created.html',
        {'order': order, 'domain': domain}
    )
    subject = f'Order #{order.id} confirmation'

    # Obtener el correo de origen desde la configuración
    from_email = settings.DEFAULT_FROM_EMAIL  # Usando la variable de entorno
    to_email = [order.email]

    # Crear correo Multipart (texto plano + HTML)
    email = EmailMultiAlternatives(
        subject,
        "Su Orden de Software ERP Business Analytics fue creado!",  # fallback texto plano
        from_email,
        to_email
    )
    email.attach_alternative(html_message, "text/html")

    # ------- Adjuntar PDF -------
    # Necesitas pasar un request simulado si tu PDF usa URLs absolutas
    from django.test import RequestFactory
    fake_request = RequestFactory().get('/')
    fake_request.META['HTTP_HOST'] = domain

    pdf_bytes = generate_order_pdf(order, fake_request)
    email.attach(f"order_{order.id}.pdf", pdf_bytes, 'application/pdf')

    email.send()

    return True
