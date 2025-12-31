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
        # Obtener nonce de Braintree
        nonce = request.POST.get('payment_method_nonce')

        if not nonce:
            return redirect('saas_payment:canceled')

        # Crear transacción en Braintree
        result = braintree.Transaction.sale({
            'amount': f"{order.get_total_cost().amount:.2f}",
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            # Marcar orden como pagada
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()

            # Crear email
            subject = f'My Shop - Invoice no. {order.id}'
            message = 'Please, find attached the invoice for your recent purchase.'
            email = EmailMessage(
                subject,
                message,
                'admin@myshop.com',
                [order.email]
            )

            # Renderizar HTML del PDF
            html = render_to_string(
                'saas_orders/order/pdf.html',
                {'order': order}
            )

            out = BytesIO()

            # 👉 GENERAR PDF (MISMO PATRÓN QUE FUNCIONA)
            weasyprint.HTML(
                string=html,
                base_url=request.build_absolute_uri()
                ).write_pdf(out,
                stylesheets=[weasyprint.CSS('saas_orders/static/css/pdf.css')])


            # Adjuntar PDF
            email.attach(
                f'order_{order.id}.pdf',
                out.getvalue(),
                'application/pdf'
            )

            # Enviar correo
            email.send()

            # Enviar contratos con Celery
            send_contracts.delay(order.id)

            return redirect('saas_payment:done')

        return redirect('saas_payment:canceled')

    # GET → mostrar formulario y generar token
    client_token = braintree.ClientToken.generate()

    return render(
        request,
        'payment/process.html',
        {
            'order': order,
            'client_token': client_token
        }
    )





@login_required
def payment_process_kushki(request):
    # Recuperamos el ID de la orden desde la sesión
    order_id = request.session.get('order_id')
    order = get_object_or_404(SaaSOrder, id=order_id)

    # Verificamos si el método de solicitud es POST
    if request.method == 'POST':
        # Recuperamos el token de pago generado por Kushki
        token = request.POST.get('token', None)

        if token:
            # Aquí debes usar la API de Kushki para realizar la transacción
            # Usamos la clave privada de Kushki para hacer la solicitud
            private_key = 'KUSHKI_PRIVATE_KEY'
            url = 'https://sandbox.kushki.com/v1/transaction/charge'

            # Datos de la transacción
            data = {
                'amount': int(order.get_total_cost() * 100),  # Monto en centavos
                'currency': 'USD',
                'token': token,
                'service': 'PRODUCTO O SERVICIO',  # Nombre del servicio o producto
            }

            headers = {
                'Authorization': f'Bearer {private_key}',
                'Content-Type': 'application/json'
            }

            # Hacemos la solicitud de la transacción a Kushki
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                # Si la transacción fue exitosa, marcamos la orden como pagada
                order.paid = True
                order.braintree_id = response.json().get('transaction_id')  # Guarda el ID de la transacción de Kushki
                order.save()

                # Creamos el correo con la factura en PDF
                subject = f'My Shop - Invoice no. {order.id}'
                message = 'Please, find attached the invoice for your recent purchase.'
                email = EmailMessage(subject,
                                     message,
                                     'admin@myshop.com',
                                     [order.email])

                # Generamos la factura en PDF
                html = render_to_string('orders/order/pdf.html', {'order': order})
                out = BytesIO()
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
                weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[weasyprint.CSS('orders/static/css/pdf.css')], presentational_hints=True)
                # Adjuntamos el archivo PDF
                email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
                # Enviamos el correo
                email.send()

                # Redirigimos a la página de "pedido realizado con éxito"
                return redirect('saas_payment:done')

            else:
                # Si la transacción falla, redirigimos a la página de cancelación
                return redirect('saas_payment:canceled')

        else:
            # Si no se recibió el token de Kushki
            return redirect('saas_payment:canceled')

    else:
        # En la primera solicitud (GET), generamos el token de cliente para Kushki
        client_token = 'GENERATE_YOUR_CLIENT_TOKEN_HERE'  # En Kushki no es necesario un ClientToken como en Braintree
        return render(request,
                      'payment/process.html',
                      {'order': order})




@login_required
def payment_done(request):
    return render(request, 'payment/done.html')

@login_required
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
