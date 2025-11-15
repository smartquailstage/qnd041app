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
    domain = "smartquail.io"

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


    # saas_orders/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import SaaSOrder

@shared_task
def deactivate_old_orders():
    """
    Marca como inactivas las órdenes que superen los 15 días de creación.
    """
    cutoff_date = timezone.now() - timedelta(days=15)
    old_orders = SaaSOrder.objects.filter(is_active=True, created__lt=cutoff_date)
    count = old_orders.update(is_active=False)
    return f'{count} órdenes desactivadas.'

from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import os
from .models import SaaSOrder

@shared_task
def send_order_email(order_id):

    try:
        order = SaaSOrder.objects.get(id=order_id)
    except SaaSOrder.DoesNotExist:
        return f"Orden {order_id} no encontrada."

    # Evitar reenvíos
    if order.email_sent:
        return f"Correo ya enviado para la orden {order_id}."

    subject = f"Gracias por su compra - SaaS Order #{order.id}"
    message = render_to_string('saas_orders/mails/payment/order_confirmation.html', {
        'order': order
    })
    
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email]
    )

    # Adjuntar contratos
    contratos_dir = os.path.join(settings.BASE_DIR, 'contracts')  # carpeta donde guardas PDFs
    for filename in os.listdir(contratos_dir):
        if filename.endswith('.pdf'):
            email.attach_file(os.path.join(contratos_dir, filename))

    email.content_subtype = "html"  # para HTML
    email.send()

    # Marcar como enviado
    order.email_sent = True
    order.save(update_fields=['email_sent'])

    return f"Correo enviado a {order.email} para la orden {order_id}."
