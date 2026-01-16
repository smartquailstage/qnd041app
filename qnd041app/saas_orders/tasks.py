from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from .models import SaaSOrder
from .utils.pdf import generate_order_pdf
from django.conf import settings  # Importar configuraciones

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import SaaSOrder
from django.conf import settings
import weasyprint
from io import BytesIO

from io import BytesIO
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task
import weasyprint
from .models import SaaSOrder

import os
from io import BytesIO
from decimal import Decimal
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import weasyprint

from .models import SaaSOrder

@shared_task
def order_created(order_id):
    order = SaaSOrder.objects.get(id=order_id)
    domain = "ec.smartquail.io"

    # Evitar errores de Fontconfig
    os.environ['FONTCONFIG_PATH'] = '/tmp/fontconfig'
    os.environ['FONTCONFIG_CACHE'] = '/tmp/fontconfig_cache'
    os.makedirs(os.environ['FONTCONFIG_CACHE'], exist_ok=True)

    # Obtener los nombres de todos los productos de la orden
    product_names = ", ".join([item.product.name for item in order.items.all()]) or "su software"

    # Render HTML correo
    html_message = render_to_string(
        'saas_orders/mails/invoices/order_created.html',
        {'order': order, 'domain': domain, 'products': order.items.all()}
    )

    # Asunto del correo
    subject = f'Su orden de compra del software {product_names} se ha completado con éxito 🎉'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [order.email]

    email = EmailMultiAlternatives(
        subject,
        "Su Orden de Software ERP Business Analytics fue creada!",
        from_email,
        to_email
    )
    email.attach_alternative(html_message, "text/html")

    # ------------------------------
    # 📄 1) Generar PDF de la orden
    # ------------------------------
    html = render_to_string('saas_orders/order/pdf2.html', {'order': order, 'domain': domain})
    out = BytesIO()

    css_path = '/qnd041app/qnd041app/saas_orders/static/css/pdf.css'

    weasyprint.HTML(string=html, base_url=f"https://{domain}/").write_pdf(
        out,
        stylesheets=[weasyprint.CSS(css_path)],
        presentational_hints=True
    )

    email.attach(f"order_{order.id}.pdf", out.getvalue(), 'application/pdf')

    # ------------------------------
    # 📘 2) Generar eBook adicional
    # ------------------------------
    ebook_html = render_to_string(
        'saas_orders/ebook/ebook_template.html',
        {'order': order, 'domain': domain}
    )

    ebook_out = BytesIO()
    ebook_css = '/qnd041app/qnd041app/saas_orders/static/css/ebook.css'

    weasyprint.HTML(string=ebook_html, base_url=f"https://{domain}/").write_pdf(
        ebook_out,
        stylesheets=[weasyprint.CSS(ebook_css)],
        presentational_hints=True
    )

    # Puedes llamarlo como quieras:
    email.attach(f"ebook_{order.id}.pdf", ebook_out.getvalue(), 'application/pdf')

    # ------------------------------
    # Enviar correo
    # ------------------------------
    email.send()

    # Marcar email como enviado
    order.email_sent = True
    order.save()

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



# saas_orders/tasks.py
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from io import BytesIO
import weasyprint
from django.conf import settings
from .models import SaaSOrder

@shared_task
def send_payment_and_contracts_email_task(order_id):
    try:
        order = SaaSOrder.objects.get(id=order_id)
        domain = 'ec.smartquail.io'

        # Render HTML del correo
        html_message = render_to_string(
            'saas_orders/mails/payment_completed.html',
            {'order': order, 'domain': domain}
        )

        subject = "✅ Pago registrado y verificación de contratos - ITC Business"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [order.email]

        email = EmailMultiAlternatives(
            subject,
            "Su pago ha sido registrado correctamente en SmartQuail Cloud.",
            from_email,
            to_email
        )
        email.attach_alternative(html_message, "text/html")

        # Adjuntar contratos no firmados
        contracts = [
            ('Contrato_IP.pdf', 'saas_orders/contracts/contract_ip.html', 'contract_hash_ip', 'contract_verified_ip'),
            ('Contrato_DEV.pdf', 'saas_orders/contracts/contract_development.html', 'contract_hash_dev', 'contract_verified_dev'),
            ('Contrato_CLOUD.pdf', 'saas_orders/contracts/contract_cloud_rent.html', 'contract_hash_cloud', 'contract_verified_cloud'),
        ]

        for filename, template, hash_field, verified_field in contracts:
            if not getattr(order, verified_field):
                # Generar hash si no existe
                if not getattr(order, hash_field):
                    generator_method = f'generate_{hash_field}'
                    if hasattr(order, generator_method):
                        setattr(order, hash_field, getattr(order, generator_method)())
                        order.save(update_fields=[hash_field])

                # Renderizar PDF
                html_contract = render_to_string(
                    template,
                    {'order': order, 'domain': domain, 'contract_hash': getattr(order, hash_field)}
                )

                out = BytesIO()
                css_path = f'saas_orders/static/css/{filename.lower().replace(".pdf", "")}.css'

                weasyprint.HTML(string=html_contract, base_url=f"https://{domain}/").write_pdf(
                    out,
                    stylesheets=[weasyprint.CSS(css_path)],
                    presentational_hints=True
                )

                email.attach(filename, out.getvalue(), 'application/pdf')

        email.send()
        order.email_sent = True
        order.save(update_fields=['email_sent'])
        return True

    except Exception as e:
        print(f"Error enviando correo de pago y contratos: {e}")
        return False
