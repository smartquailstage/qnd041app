from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from .models import PaaSOrder
from .utils.pdf import generate_order_pdf
from django.conf import settings  # Importar configuraciones

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings
import weasyprint
from io import BytesIO

from io import BytesIO
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task
import weasyprint


import os
from io import BytesIO
from decimal import Decimal
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import weasyprint

import requests
from decimal import Decimal
from django.conf import settings
from django.urls import reverse

from saas_orders.models import SaaSOrder
import requests

from celery import shared_task
from django.conf import settings
from django.urls import reverse

from paas_orders.models import PaaSOrder


@shared_task
def enviar_whatsapp_orden(order_id):

    try:
        order = PaaSOrder.objects.get(id=order_id)

    except PaaSOrder.DoesNotExist:
        return "Orden no encontrada"

    domain = "ec.smartquail.io"

    # ==================================================
    # URLs SEGURAS
    # ==================================================

    try:
        pdf_url = (
            f"{domain}"
            f"{reverse('paas_orders:admin_order_pdf', kwargs={'order_id': order.id})}"
        )
    except Exception:
        pdf_url = f"{domain}"

    try:
        order_url = (
            f"https://{domain}"
            f"{reverse('paas_orders:order_detail', kwargs={'order_id': order.id})}"
        )
    except Exception:
        order_url = f"https://{domain}"

    # ==================================================
    # DATOS SEGUROS
    # ==================================================

    telefono = str(order.telefono or "").replace("+", "").strip()

    nombre_cliente = (
        f"{order.first_name or ''} {order.last_name or ''}".strip()
        or "Cliente SmartQuail"
    )

    codigo_convenio = (
        order.coupon.code
        if order.coupon and order.coupon.code
        else "Sin convenio"
    )

    descuento = f"{order.discount or 0}%"

    productos = (
        ", ".join(
            [item.product.name for item in order.items.all() if item.product]
        ) or "Software SmartQuail"
    )

    estado_pago = "Pagado" if order.paid else "Pendiente"

    # ==================================================
    # HELPERS MONEY SAFE
    # ==================================================

    def money(value):
        try:
            return f"{float(value or 0):.2f} USD"
        except Exception:
            return "0.00 USD"

    subtotal = money(order.get_subtotal())
    iva = money(order.get_total_iva())
    total = money(order.get_total_with_discount())
    total_credito = money(order.get_total_with_discount_interes())
    mensualidad = money(order.get_total_monthly_suscription())

    # ==================================================
    # WHATSAPP CLOUD API
    # ==================================================

    url = (
        f"https://graph.facebook.com/v20.0/"
        f"{settings.TWILIO_ACCOUNT_SID}/messages"
    )

    headers = {
        "Authorization": f"Bearer {settings.N8N_WEBHOOK_URL}",
        "Content-Type": "application/json"
    }

    # ==================================================
    # TEMPLATE PARAMETERS
    # ==================================================

    parametros_template = [
        {"type": "text", "parameter_name": "nombre_cliente", "text": nombre_cliente},
        {"type": "text", "parameter_name": "numero_orden", "text": str(order.id)},
        {"type": "text", "parameter_name": "pdf_url", "text": pdf_url},

    ]

    # ==================================================
    # PAYLOAD
    # ==================================================

    data = {
        "messaging_product": "whatsapp",
        "to": telefono,
        "type": "template",
        "template": {
            "name": "adquisicion_de_licencia_plt",
            "language": {
                "code": "es_EC"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": parametros_template
                }
            ]
        }
    }

    # ==================================================
    # REQUEST
    # ==================================================

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=30
        )

        response_data = response.json()
        
        print("WHATSAPP RESPONSE:", response_data)
        
        return {
            "status_code": response.status_code,
            "response": response_data
        }

    except Exception as e:
        return {
            "error": str(e)
        }







@shared_task
def order_created(order_id):
    order = PaaSOrder.objects.get(id=order_id)
    domain = "ec.smartquail.io"

    # Evitar errores de Fontconfig
    os.environ['FONTCONFIG_PATH'] = '/tmp/fontconfig'
    os.environ['FONTCONFIG_CACHE'] = '/tmp/fontconfig_cache'
    os.makedirs(os.environ['FONTCONFIG_CACHE'], exist_ok=True)

    # Obtener los nombres de todos los productos de la orden
    product_names = ", ".join([item.product.name for item in order.items.all()]) or "su software"

    # Render HTML correo
    html_message = render_to_string(
        'paas_orders/mails/invoices/order_created.html',
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
    html = render_to_string('paas_orders/order/pdf2.html', {'order': order, 'domain': domain})
    out = BytesIO()

    css_url = "https://qnd03101.sfo3.digitaloceanspaces.com/qnd03101/qnd041app/static/css/pdf.css"

    weasyprint.HTML(string=html, base_url=f"https://{domain}/").write_pdf(
        out,
        stylesheets=[weasyprint.CSS(css_url)],
        presentational_hints=True
    )

    email.attach(f"order_{order.id}.pdf", out.getvalue(), 'application/pdf')



    # ------------------------------
    # Enviar correo
    # ------------------------------
    email.send()

    # Marcar email como enviado
    order.email_sent = True
    order.save()

    return True



import requests
from decimal import Decimal
from django.conf import settings
from django.urls import reverse

from paas_orders.models import PaaSOrder

@shared_task
def enviar_whatsapp_orden_paas(order_id):

    try:
        order = PaaSOrder.objects.get(id=order_id)
    except PaaSOrder.DoesNotExist:
        return "Orden no encontrada"

    domain = "ec.smartquail.io"

    # ==================================================
    # URLs
    # ==================================================
    pdf_url = (
        f"https://{domain}"
        f"{reverse('paas_orders:order_pdf', kwargs={'order_id': order.id})}"
    )

    order_url = (
        f"https://{domain}"
        f"{reverse('paas_orders:order_detail', kwargs={'order_id': order.id})}"
    )

    # ==================================================
    # DATOS SEGUROS (SIN NULL)
    # ==================================================
    telefono = str(order.telefono).replace("+", "").strip()

    nombre_cliente = (
        f"{order.first_name or ''} {order.last_name or ''}".strip()
        or "Cliente SmartQuail"
    )

    email_cliente = order.email or "No registrado"

    razon_social = order.razon_social or "No registrada"

    ruc = order.ruc or "No registrado"

    sector = order.get_sector_display() if order.sector else "No especificado"

    codigo_convenio = (
        order.coupon.code
        if order.coupon and order.coupon.code
        else "Sin convenio"
    )

    descuento = (
        f"{order.discount}%"
        if order.discount
        else "0%"
    )

    subtotal = (
        str(order.get_subtotal())
        if order.get_subtotal()
        else "0.00 USD"
    )

    iva = (
        f"{order.get_total_iva():.2f} USD"
        if order.get_total_iva()
        else "0.00 USD"
    )

    total = (
        f"{order.get_total_with_discount():.2f} USD"
        if order.get_total_with_discount()
        else "0.00 USD"
    )

    total_credito = (
        f"{order.get_total_with_discount_interes()} USD"
        if order.get_total_with_discount_interes()
        else "0.00 USD"
    )

    mensualidad = (
        f"{order.get_total_monthly_suscription()} USD"
        if order.get_total_monthly_suscription()
        else "0.00 USD"
    )

    estado_pago = "Pagado" if order.paid else "Pendiente"

    productos = (
        ", ".join(
            [item.product.name for item in order.items.all()]
        )
        or "Software SmartQuail"
    )

    # ==================================================
    # WHATSAPP CLOUD API
    # ==================================================
    url = (
        f"https://graph.facebook.com/v20.0/"
        f"{settings.TWILIO_ACCOUNT_SID}/messages"
    )

    headers = {
        "Authorization": f"Bearer {settings.N8N_WEBHOOK_URL}",
        "Content-Type": "application/json"
    }

    # ==================================================
    # TEMPLATE PARAMETERS
    # ==================================================
    parametros_template = [
        {
            "type": "text",
            "parameter_name": "nombre_cliente",
            "text": nombre_cliente
        },
        {
            "type": "text",
            "parameter_name": "numero_orden",
            "text": str(order.id)
        },
        {
            "type": "text",
            "parameter_name": "productos",
            "text": productos
        },
        {
            "type": "text",
            "parameter_name": "subtotal",
            "text": subtotal
        },
        {
            "type": "text",
            "parameter_name": "iva",
            "text": iva
        },
        {
            "type": "text",
            "parameter_name": "total",
            "text": total
        },
        {
            "type": "text",
            "parameter_name": "codigo_convenio",
            "text": codigo_convenio
        },
        {
            "type": "text",
            "parameter_name": "descuento",
            "text": descuento
        },
        {
            "type": "text",
            "parameter_name": "estado_pago",
            "text": estado_pago
        },
        {
            "type": "text",
            "parameter_name": "mensualidad",
            "text": mensualidad
        },
        {
            "type": "text",
            "parameter_name": "total_credito",
            "text": total_credito
        },
        {
            "type": "text",
            "parameter_name": "pdf_url",
            "text": pdf_url
        },
        {
            "type": "text",
            "parameter_name": "order_url",
            "text": order_url
        }
    ]

    # ==================================================
    # PAYLOAD
    # ==================================================
    data = {
        "messaging_product": "whatsapp",
        "to": telefono,
        "type": "template",
        "template": {
            "name": "adquisicion_de_licencia_plt",
            "language": {
                "code": "es_AR"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": parametros_template
                }
            ]
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    return response.json()




    # saas_orders/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta


@shared_task
def deactivate_old_orders():
    """
    Marca como inactivas las órdenes que superen los 15 días de creación.
    """
    cutoff_date = timezone.now() - timedelta(days=15)
    old_orders = PaaSOrder.objects.filter(is_active=True, created__lt=cutoff_date)
    count = old_orders.update(is_active=False)
    return f'{count} órdenes desactivadas.'

from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import os

@shared_task
def send_order_email(order_id):

    try:
        order = PaaSOrder.objects.get(id=order_id)
    except PaaSOrder.DoesNotExist:
        return f"Orden {order_id} no encontrada."

    # Evitar reenvíos
    if order.email_sent:
        return f"Correo ya enviado para la orden {order_id}."

    subject = f"Gracias por su compra - PaaS Order #{order.id}"
    message = render_to_string('paas_orders/mails/payment/order_confirmation.html', {
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

@shared_task
def send_payment_and_contracts_email_task(order_id):
    try:
        order = PaaSOrder.objects.get(id=order_id)
        domain = 'ec.smartquail.io'

        # Render HTML del correo
        html_message = render_to_string(
            'paas_orders/mails/payment_completed.html',
            {'order': order, 'domain': domain}
        )

        subject = "✅ Pago registrado y verificación de contratos - ITC Business"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [order.email,settings.DEFAULT_FROM_EMAIL]

        email = EmailMultiAlternatives(
            subject,
            "Su pago ha sido registrado correctamente en SmartQuail Cloud.",
            from_email,
            to_email
        )
        email.attach_alternative(html_message, "text/html")

        # Adjuntar contratos no firmados
        contracts = [
            ('Contrato_IP.pdf', 'paas_orders/contracts/contract_ip.html', 'contract_hash_ip', 'contract_verified_ip'),
            ('Contrato_DEV.pdf', 'paas_orders/contracts/contract_development.html', 'contract_hash_dev', 'contract_verified_dev'),
            ('Contrato_CLOUD.pdf', 'paas_orders/contracts/contract_cloud_rent.html', 'contract_hash_cloud', 'contract_verified_cloud'),
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
                css_path = f'paas_orders/static/css/{filename.lower().replace(".pdf", "")}.css'

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


from celery import shared_task

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import PaaSOrder


@shared_task
def send_project_manager_email(order_id):

    try:
        order = PaaSOrder.objects.select_related(
            "project_manager"
        ).prefetch_related(
            "items"
        ).get(id=order_id)

    except PaaSOrder.DoesNotExist:
        return

    # Evitar reenvíos
    if order.email_sent:
        return

    # Validaciones
    if not order.project_manager:
        return

    if not order.project_manager.email:
        return

    # Obtener dominio automáticamente
    current_site = Site.objects.get_current()
    domain = current_site.domain

    subject = f"Nueva orden PaaS #{order.id}"

    html_content = render_to_string(
        "paas_orders/mails/project_manager_notification.html",
        {
            "order": order,
            "domain": domain,
        }
    )

    message = EmailMultiAlternatives(
        subject=subject,
        body="Nueva orden PaaS asignada.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.project_manager.email],
    )

    message.attach_alternative(html_content, "text/html")
    message.send()

    # Marcar enviado
    order.email_sent = True
    order.save(update_fields=["email_sent"])

    try:
        order = PaaSOrder.objects.select_related(
            "project_manager"
        ).prefetch_related(
            "items"
        ).get(id=order_id)

    except PaaSOrder.DoesNotExist:
        return

    if order.email_sent:
        return

    if not order.project_manager:
        return

    if not order.project_manager.email:
        return

    subject = f"Nueva orden PaaS #{order.id}"

    html_content = render_to_string(
        "paas_orders/sqcrew/project_manager.html",
        {
            "order": order,
            "domain": domain,
        }
    )

    message = EmailMultiAlternatives(
        subject=subject,
        body="Nueva orden PaaS asignada.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.project_manager.email],
    )

    message.attach_alternative(html_content, "text/html")
    message.send()

    order.email_sent = True
    order.save(update_fields=["email_sent"])