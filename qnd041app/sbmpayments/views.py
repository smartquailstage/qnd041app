import braintree
from django.shortcuts import render, redirect, get_object_or_404 
from sbmorders.models import Order, BankTransfer
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO
import paypalrestsdk
from django.urls import reverse
import requests
from django.contrib import messages
from django.http import HttpResponse


def amazon_pay_cancel(request):
    messages.warning(request, "El pago fue cancelado.")
    return redirect('sbmpayments:order_create')


def amazon_pay_done(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'sbmpayments/amazon_pay_done.html', {'order': order})


def amazon_pay_execute(request, order_id):
    checkout_session_id = request.GET.get('checkoutSessionId')
    order = Order.objects.get(id=order_id)

    # Construir la URL para confirmar la orden de pago
    url = f"{settings.AMAZON_PAY_ENDPOINT}/sandbox/v2/checkoutSessions/{checkout_session_id}"

    headers = {
        "Content-Type": "application/json",
        "x-amz-pay-merchant-id": settings.AMAZON_PAY_MERCHANT_ID,
        "x-amz-pay-access-key": settings.AMAZON_PAY_ACCESS_KEY,
        "x-amz-pay-secret-key": settings.AMAZON_PAY_SECRET_KEY,
    }

    try:
        # Enviar la solicitud para confirmar la transacción
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if response.status_code == 200 and response_data.get("status") == "OPEN":
            # Cambiar el estado de la orden a 'Completado'
            order.status = 'Completed'
            order.paid = True  # Marcar como pagado
            order.save()

            # Enviar correos electrónicos con los PDFs
            send_payment_emails(order, request)

            messages.success(request, "El pago fue procesado exitosamente.")
            return redirect('sbmpayments:amazon_pay_done', order_id=order.id)
        else:
            messages.error(request, "Hubo un error al confirmar el pago con Amazon Pay.")
            return redirect('sbmorders:order_create')

    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error al confirmar el pago con Amazon Pay: {e}")
        return redirect('sbmorders:order_create')


def amazon_pay_process(request, order_id):
    order = Order.objects.get(id=order_id)

    # Construir la URL para la creación de la orden de pago
    url = f"{settings.AMAZON_PAY_ENDPOINT}/sandbox/v2/checkoutSessions"

    headers = {
        "Content-Type": "application/json",
        "x-amz-pay-merchant-id": settings.AMAZON_PAY_MERCHANT_ID,
        "x-amz-pay-access-key": settings.AMAZON_PAY_ACCESS_KEY,
        "x-amz-pay-secret-key": settings.AMAZON_PAY_SECRET_KEY,
    }

    body = {
        "totalAmount": {
            "currencyCode": "USD",
            "value": str(order.get_total_cost())
        },
        "merchantOrderReference": str(order.id),
        "transactionTimeout": 3600,
    }

    try:
        # Enviar la solicitud para crear la orden
        response = requests.post(url, headers=headers, json=body)
        response_data = response.json()

        if response.status_code == 200:
            amazon_url = response_data["checkoutUrl"]
            return redirect(amazon_url)
        else:
            messages.error(request, "Error al crear la orden en Amazon Pay.")
            return redirect('sbmorders:order_create')

    except requests.exceptions.RequestException as e:
        messages.error(request, f"Hubo un error al procesar el pago con Amazon Pay: {e}")
        return redirect('sbmorders:order_create')


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {'submit_for_settlement': True}
        })

        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()

            # Enviar correos electrónicos con los PDFs
            send_payment_emails(order, request)

            return redirect('saas_payments:done')
        else:
            return redirect('saas_payments:canceled')
    else:
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html', {'order': order, 'client_token': client_token})


def send_payment_emails(order, request):
    """
    Función que maneja el envío de los correos electrónicos con los PDFs adjuntos.
    """
    subject = f'My Shop - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])

    # Generar el primer PDF (Invoice)
    html = render_to_string('sbmorders/order/pdf.html', {'order': order})
    out_invoice = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[weasyprint.CSS('sbmorders/static/css/pdf.css')])
    email.attach(f'order_{order.id}.pdf', out_invoice.getvalue(), 'application/pdf')

    # Generar PDF adicional (Resumen de la orden)
    out_summary = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_summary_{order.id}.pdf'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[weasyprint.CSS('sbmorders/static/css/pdf.css')])
    email.attach(f'order_summary_{order.id}.pdf', out_summary.getvalue(), 'application/pdf')

    # Términos y condiciones PDF
    html = render_to_string('sbmorders/order/terms_pdf.html', {'order': order})
    out_terms = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}_terms.pdf'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[weasyprint.CSS('sbmorders/static/css/pdf.css')])
    email.attach(f'terms_and_conditions_{order.id}.pdf', out_terms.getvalue(), 'application/pdf')

    # Enviar el correo con los archivos adjuntos
    email.send()


def paypal_done(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'sbmpayments/paypal_done.html', {'order': order})


def paypal_cancel(request):
    messages.warning(request, "El pago ha sido cancelado.")
    return redirect('sbmpayments:order_create')


def paypal_execute(request, order_id):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    order = Order.objects.get(id=order_id)
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({'payer_id': payer_id}):
        order.status = 'Completed'
        order.paid = True  # Marcar la orden como pagada
        order.save()

        # Enviar correos electrónicos con los PDFs
        send_payment_emails(order, request)

        messages.success(request, f"El pago de la orden {order.id} se ha procesado correctamente.")
        return redirect('sbmpayments:paypal_done', order_id=order.id)
    else:
        messages.error(request, f"Hubo un error al procesar el pago de la orden {order.id}.")
        return redirect('sbmpayments:paypal_cancel')


# Procesos para PayPal, AmazonPay y ApplePay
def paypal_process(request, order_id):
    order = Order.objects.get(id=order_id)

    payment = paypalrestsdk.Payment({
        'intent': 'sale',
        'payer': {'payment_method': 'paypal'},
        'transactions': [{
            'amount': {'total': str(order.get_total_cost()), 'currency': 'USD'},
            'description': f'Orden #{order.id}'
        }],
        'redirect_urls': {
            'return_url': request.build_absolute_uri(reverse('sbmpayments:paypal_execute', args=[order.id])),
            'cancel_url': request.build_absolute_uri(reverse('sbmpayments:paypal_cancel'))
        }
    })

    if payment.create():
        for link in payment.links:
            if link.rel == 'approval_url':
                approval_url = link.href
                return redirect(approval_url)
    else:
        return render(request, 'sbmpayments/paypal_error.html', {'error': 'Error al crear la orden de PayPal.'})



def transfer_confirmations(request, order_id):
    try:
        # Intentamos obtener la orden por el order_id
        order = Order.objects.get(id=order_id)

        # Obtenemos la transferencia bancaria asociada con esta orden
        bank = BankTransfer.objects.get(order=order)

    except Order.DoesNotExist:
        # Si la orden no existe, mostramos un mensaje de error y redirigimos
        messages.error(request, "Pedido no encontrado.")
        return redirect('home')  # Redirige a la página de inicio o la página deseada

    except BankTransfer.DoesNotExist:
        # Si no existe una transferencia bancaria asociada a esta orden, mostramos un mensaje
        messages.error(request, "No se ha encontrado información de pago para este pedido.")
        return redirect('home')  # Redirige a la página de inicio o la página deseada

    # Si la orden y la transferencia bancaria existen, procedemos a mostrar la página de confirmación
    return render(request, 'payment/done_trans.html', {
        'order': order,
        'bank': bank,
    })


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')


#PayPal payment gateway     


def paypal_done(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'sbmpayments/paypal_done.html', {'order': order})

def paypal_cancel(request):
    messages.warning(request, "El pago ha sido cancelado.")
    return redirect('sbmpayments:order_create')


def paypal_execute(request, order_id):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    # Obtener la orden de la base de datos
    order = Order.objects.get(id=order_id)

    # Obtener el pago desde PayPal y ejecutarlo
    payment = paypalrestsdk.Payment.find(payment_id)
    
    if payment.execute({'payer_id': payer_id}):
        order.status = 'Completed'
        order.save()

        # Realiza las acciones post-pago: enviar confirmación, email, etc.
        # (Ejemplo: enviar un email o realizar alguna tarea)
        
        messages.success(request, f"El pago de la orden {order.id} se ha procesado correctamente.")

        return redirect('sbmpayments:paypal_done', order_id=order.id)
    else:
        messages.error(request, f"Hubo un error al procesar el pago de la orden {order.id}.")
        return redirect('sbmpayments:paypal_cancel')


# Procesos para PayPal, AmazonPay y ApplePay
def paypal_process(request, order_id):
    order = Order.objects.get(id=order_id)

    # Crear una orden en PayPal
    payment = paypalrestsdk.Payment({
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal'
        },
        'transactions': [{
            'amount': {
                'total': str(order.get_total_cost()),  # Suponiendo que tienes un método que calcula el total
                'currency': 'USD'
            },
            'description': f'Orden #{order.id}'
        }],
        'redirect_urls': {
            'return_url': request.build_absolute_uri(reverse('sbmpayments:paypal_execute', args=[order.id])),
            'cancel_url': request.build_absolute_uri(reverse('sbmpayments:paypal_cancel'))
        }
    })

    if payment.create():
        for link in payment.links:
            if link.rel == 'approval_url':
                approval_url = link.href
                return redirect(approval_url)
    else:
        return render(request, 'sbmpayments/paypal_error.html', {'error': 'Error al crear la orden de PayPal.'})