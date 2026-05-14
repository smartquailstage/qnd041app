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
from django.shortcuts import get_object_or_404
import os
import io
import base64
import qrcode

from django.urls import reverse

from django.contrib.staticfiles import finders


import os
import io
import base64
import qrcode

from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse

import weasyprint

from .models import SaaSOrder


from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from pathlib import Path
from io import BytesIO

import os
import io
import base64
import qrcode
import weasyprint

from saas_orders.models import SaaSOrder


@shared_task(bind=True, max_retries=3)
def order_created(self, order_id):

    # ------------------------------------------------
    # 🔎 Obtener orden
    # ------------------------------------------------
    try:
        order = (
            SaaSOrder.objects
            .select_related('user')
            .prefetch_related('items__product')
            .get(id=order_id)
        )
    except SaaSOrder.DoesNotExist:
        return False

    # ------------------------------------------------
    # 📧 Validar email
    # ------------------------------------------------
    if not order.email:
        return False

    domain = "ec.smartquail.io"

    # ------------------------------------------------
    # 🧠 Configuración Fontconfig / WeasyPrint
    # ------------------------------------------------
    font_cache = "/tmp/fontconfig"

    os.makedirs(font_cache, exist_ok=True)

    os.environ["XDG_CACHE_HOME"] = font_cache
    os.environ["FC_CACHEDIR"] = font_cache

    # ------------------------------------------------
    # 📦 Items
    # ------------------------------------------------
    items = list(order.items.all())

    product_names = ", ".join(
        [
            item.product.name
            for item in items
            if item.product
        ]
    ) or "su software"

    # ------------------------------------------------
    # 📩 HTML correo
    # ------------------------------------------------
    html_message = render_to_string(
        'saas_orders/mails/invoices/order_created.html',
        {
            'order': order,
            'domain': domain,
            'items': items
        }
    )

    subject = (
        f'Su orden de compra del software '
        f'{product_names} se ha completado con éxito 🎉'
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body="Su Orden de Software ERP Business Analytics fue creada!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.email, settings.DEFAULT_FROM_EMAIL ]
    )

    email.attach_alternative(html_message, "text/html")

    # ------------------------------------------------
    # 📌 QR
    # ------------------------------------------------
    try:
        url = (
            f"https://{domain}"
            f"{reverse('saas_orders:order_detail', kwargs={'order_id': order.id})}"
        )
    except Exception:
        url = f"https://{domain}"

    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1,
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="#4d4d4d",
        back_color="#E5E1E1"
    )

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode()

    qr_url = f"data:image/png;base64,{qr_base64}"

    buffer.close()

    # ------------------------------------------------
    # 📄 HTML PDF
    # ------------------------------------------------
    pdf_html = render_to_string(
        'saas_orders/order/pdf2.html',
        {
            'order': order,
            'domain': domain,
            'qr_url': qr_url,
        }
    )

    out = BytesIO()

    # ------------------------------------------------
    # ✅ CSS local real
    # ------------------------------------------------
    css_path = finders.find("css/pdf.css")
    # ------------------------------------------------
    # ✅ Base URL local
    # ------------------------------------------------
    base_url = settings.BASE_DIR

    # ------------------------------------------------
    # ✅ Generar PDF
    # ------------------------------------------------
    try:

        weasyprint.HTML(
            string=pdf_html,
            base_url=str(base_url)
        ).write_pdf(
            target=out,
            stylesheets=[
                weasyprint.CSS(
                    filename=css_path
                )
            ],
            presentational_hints=True
        )

    except Exception as e:
        print(f"ERROR GENERANDO PDF: {e}")
        raise self.retry(exc=e, countdown=10)

    # ------------------------------------------------
    # 📎 Adjuntar PDF
    # ------------------------------------------------
    email.attach(
        filename=f"SQ02-APP-12{ order.id }-QND0101{order.id}.pdf",
        content=out.getvalue(),
        mimetype='application/pdf'
    )

    out.close()

    # ------------------------------------------------
    # 📤 Enviar correo
    # ------------------------------------------------
    try:
        email.send()

    except Exception as e:
        print(f"ERROR ENVIANDO EMAIL: {e}")
        raise self.retry(exc=e, countdown=10)

    # ------------------------------------------------
    # ✔️ Marcar enviado
    # ------------------------------------------------
    order.email_sent = True
    order.save(update_fields=['email_sent'])

    return True

    # ------------------------------
    # 📘 2) Generar eBook adicional
    # ------------------------------
#    ebook_html = render_to_string(
#        'saas_orders/ebook/ebook_template.html',
#        {'order': order, 'domain': domain}
#    )

#    ebook_out = BytesIO()
#    ebook_css = '/qnd041app/qnd041app/saas_orders/static/css/ebook.css'

#    weasyprint.HTML(string=ebook_html, base_url=f"https://{domain}/").write_pdf(
#        ebook_out,
#        stylesheets=[weasyprint.CSS(ebook_css)],
#        presentational_hints=True
#    )

    # Puedes llamarlo como quieras:
#    email.attach(f"ebook_{order.id}.pdf", ebook_out.getvalue(), 'application/pdf')

    # ------------------------------
    # Enviar correo
    # ------------------------------

import requests
from decimal import Decimal
from django.conf import settings
from django.urls import reverse

from saas_orders.models import SaaSOrder

@shared_task
def enviar_whatsapp_orden(order_id):

    try:
        order = SaaSOrder.objects.get(id=order_id)
    except SaaSOrder.DoesNotExist:
        return "Orden no encontrada"

    domain = "ec.smartquail.io"

    # ==================================================
    # URLs
    # ==================================================
    pdf_url = (
        f"https://{domain}"
        f"{reverse('saas_orders:order_pdf', kwargs={'order_id': order.id})}"
    )

    order_url = (
        f"https://{domain}"
        f"{reverse('saas_orders:order_detail', kwargs={'order_id': order.id})}"
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
            "name": "adquisicion_de_licencia_app",
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
