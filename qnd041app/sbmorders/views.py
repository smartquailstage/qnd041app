import qrcode
import base64
from io import BytesIO
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import OrderItem, Order, BankTransfer
from sbmshop.models import SBMProduct
from .forms import OrderCreateForm, PaymentMethodForm, BankTransferForm
from sbmcart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .tasks import order_created, generate_pdf_and_send_email
from django.core.mail import EmailMessage
from .forms import BankTransferForm
from django.contrib import messages
from django.template.loader import render_to_string
import weasyprint










def amazon_pay_process(request, order_id):
    # Aquí es donde integrarías Amazon Pay. Simulamos la redirección para el pago.
    order = Order.objects.get(id=order_id)
    # Lógica de Amazon Pay, redirigiría al usuario a Amazon para el pago
    return render(request, 'sbmpayments/amazon_pay.html', {'order': order})

def apple_pay_process(request, order_id):
    # Aquí es donde integrarías Apple Pay. Simulamos la redirección para el pago.
    order = Order.objects.get(id=order_id)
    # Lógica de Apple Pay, redirigiría al usuario a Apple Pay para el pago
    return render(request, 'sbmpayments/apple_pay.html', {'order': order})



def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        payment_form = PaymentMethodForm(request.POST)
        
        if form.is_valid() and payment_form.is_valid():
            order = form.save(commit=False)
            # Crear la orden
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()  # Vaciar el carrito
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            
            # Guardar la selección del método de pago
            payment_method = payment_form.cleaned_data['payment_method']
            if payment_method == 'card':
                return redirect(reverse('sbmpayments:process'))
            elif payment_method == 'bank_transfer':
                return redirect('sbmorders:bank_transfer_process', order_id=order.id)
            elif payment_method == 'paypal':
                return redirect('sbmpayments:paypal_process', order_id=order.id)
            elif payment_method == 'amazon_pay':
                return redirect('sbmpayments:amazon_pay_process', order_id=order.id)
            elif payment_method == 'apple_pay':
                return redirect('sbmpayments:apple_pay_process', order_id=order.id)
        
    else:
        form = OrderCreateForm()
        payment_form = PaymentMethodForm()

    # Obtener las tecnologías asociadas a los productos del carrito
    products_with_technologies = []
    for item in cart:
        product = get_object_or_404(SBMProduct, id=item['product'].id)
        technologies = product.technologies_products.all()
        products_with_technologies.append({
            'product': product,
            'technologies': technologies
        })

    return render(request, 'sbmorders/order/create.html', {
        'cart': cart,
        'form': form,
        'payment_form': payment_form,
        'products_with_technologies': products_with_technologies,
    })

def bank_transfer_process(request, order_id):
    # Obtener la orden, devolver 404 si no se encuentra
    order = get_object_or_404(Order, id=order_id)

    # Obtener los ítems de la orden
    order_items = order.items.all()  # Suponiendo que hay una relación en el modelo Order con OrderItem

    # Generar el contenido del QR (enlace al pago)
    qr_data = f'https://tusitio.com/pago/{order_id}'

    # Crear el QR con un tamaño mediano
    qr = qrcode.QRCode(
        version=1,  # Controla el tamaño general del QR, entre 1 (más pequeño) y 40 (más grande)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivel de corrección de errores
        box_size=5,  # Ajusta el tamaño de cada "caja" en el código QR
        border=4  # Ajusta el tamaño del borde
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Generar la imagen del QR
    img = qr.make_image(fill='black', back_color='Lightgray')

    # Guardar el código QR en un buffer en memoria
    qr_buffer = BytesIO()
    img.save(qr_buffer)
    qr_buffer.seek(0)

    # Codificar el QR en base64 para poder pasarlo a la plantilla
    qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')

    # Procesar el formulario si es un POST
    if request.method == 'POST':
        form = BankTransferForm(request.POST)
        if form.is_valid():
            # Guardar la transferencia bancaria y asociarla a la orden
            bank_transfer = form.save(commit=False)
            bank_transfer.order = order
            bank_transfer.save()

            # Enviar el PDF generado por la tarea en segundo plano (usando Celery)
            generate_pdf_and_send_email.delay(order.id)  # Usamos Celery para enviar el PDF por email

            # Mostrar mensaje de éxito
            messages.success(request, "La transferencia bancaria se ha procesado correctamente.")

            # Redirigir al usuario a la página de confirmación, pasando el order_id
            return redirect(reverse('sbmpayments:done_trans', args=[order.id]))

    else:
        form = BankTransferForm()

    # Pasar los ítems de la orden y el QR al contexto para renderizarla en la plantilla
    return render(request, 'sbmorders/order/bank_transfer.html', {
        'order': order,
        'form': form,
        'qr_code_base64': qr_base64,   # Pasamos el QR como valor binario
        'order_items': order_items    # Pasamos los ítems de la orden
    })






@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/sbmorders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('sbmorders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html,  base_url=request.build_absolute_uri() ).write_pdf(response,stylesheets=[weasyprint.CSS('sbmorders/static/css/pdf.css')], presentational_hints=True)
    return response
