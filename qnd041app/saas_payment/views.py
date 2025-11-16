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


from django.shortcuts import get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO
import weasyprint
from saas_orders.models import SaaSOrder
from celery.result import AsyncResult
from .tasks import send_contracts  # Importa la tarea

@login_required
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(SaaSOrder, id=order_id)

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = braintree.Transaction.sale({
            'amount': f"{order.get_total_cost().amount:.2f}",  # <-- f-string con .amount
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()

            # Enviar factura por correo
            subject = f'My Shop - Invoice no. {order.id}'
            message = 'Please, find attached the invoice for your recent purchase.'
            email = EmailMessage(subject,
                                 message,
                                 'admin@myshop.com',
                                 [order.email])

            # Generar PDF
            html = render_to_string('saas_orders/order/pdf.html', {'order': order})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out,
                                                   stylesheets=stylesheets)
            # Adjuntar PDF
            email.attach(f'order_{order.id}.pdf',
                         out.getvalue(),
                         'application/pdf')
            # Enviar el correo
            email.send()

            # Llamar a la tarea de Celery para enviar los contratos
            send_contracts.delay(order.id)

            return redirect('saas_payment:done')
        else:
            return redirect('saas_payment:canceled')
    else:
        # generar token
        client_token = braintree.ClientToken.generate()
        return render(request, 
                      'payment/process.html', 
                      {'order': order,
                       'client_token': client_token})





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
