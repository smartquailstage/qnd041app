import braintree
from django.shortcuts import render, redirect, get_object_or_404 
from saas_orders.models import SaaSOrder 
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
import requests


from io import BytesIO
from io import BytesIO

from io import BytesIO

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

import weasyprint
import braintree

from saas_orders.models import SaaSOrder
from saas_payment.tasks import send_contracts






@login_required
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(SaaSOrder, id=order_id)

    if request.method == 'POST':
        token = request.POST.get('token')

        if not token:
            return redirect('saas_payment:canceled')

        # 💡 Usa tu PRIVATE KEY real de Kushki
        private_key = settings.KUSHKI_PRIVATE_KEY
        url = settings.KUSHKI_CHARGE_URL  # Ej: 'https://sandbox.kushki.com/v1/charges'

        # Montos en Kushki deben enviarse en **centavos**
        amount_cents = int(order.get_total_cost().amount * 100)

        payload = {
            "amount": amount_cents,
            "currency": "USD",
            "token": token
        }

        headers = {
            "Authorization": f"Bearer {private_key}",
            "Content-Type": "application/json"
        }

        res = requests.post(url, json=payload, headers=headers)
        data = res.json()

        if res.status_code == 200 and data.get("status") in ("AUTHORIZED", "APPROVED", "SUCCESS"):
            # Guardar transacción
            order.paid = True
            order.kushki_id = data.get("ticket") or data.get("transactionId") or data.get("reference")
            order.save()

            # 🧾 Enviar factura por email (igual que Braintree)
            subject = f'My Shop - Invoice no. {order.id}'
            message = 'Please find attached your receipt.'
            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [order.email])

            html = render_to_string('saas_orders/order/pdf.html', {'order': order})
            out = BytesIO()

            weasyprint.HTML(
                string=html,
                base_url=request.build_absolute_uri()
            ).write_pdf(out, stylesheets=[weasyprint.CSS('saas_orders/static/css/pdf.css')])

            email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
            email.send()

            return redirect('saas_payment:done')

        return redirect('saas_payment:canceled')

    # GET → Renderizar página con formulario de Kushki
    return render(request, 'payment/process.html', {'order': order})




@login_required
def payment_done(request):
    return render(request, 'payment/done.html')

@login_required
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
