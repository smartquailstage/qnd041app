from django.urls import reverse
from django.shortcuts import render, redirect
from .models import SaaSOrderItem
from .forms import OrderCreateForm
from saas_cart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import SaaSOrder
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from django.contrib.auth.decorators import login_required
from usuarios.models import Profile  







@login_required
def order_create(request):
    user = request.user
    profile = user.profile  # O `Profile.objects.get(user=user)`
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            # Si el formulario es válido, procesar la orden
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.user = user
            order.first_name = user.first_name
            order.last_name = user.last_name
            order.email = user.email

            order.save()

            for item in cart:
                SaaSOrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
            
            # Limpiar el carrito
            cart.clear()
            
            # Lanzar tarea asincrónica
            order_created.delay(order.id)
            
            # Guardar la orden en la sesión
            request.session['order_id'] = order.id
            
            # Redirigir al pago
            return redirect(reverse('saas_payment:process'))
        else:
            # Si el formulario no es válido, agregar un mensaje de error
            print("Formulario no válido")
            # Puedes agregar más detalles para depurar aquí
            print(form.errors)
    else:
        form = OrderCreateForm()

    # Aquí pasamos el objeto order al contexto
    return render(request,
                  'saas_orders/order/create.html',
                  {'cart': cart, 'form': form})



@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(SaaSOrder, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    sblorder = get_object_or_404(SaaSOrder, id=order_id)
    html = render_to_string('sblorders/order/pdf.html',
                            {'sblorder': sblorder})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(sblorder.id)
    weasyprint.HTML(string=html,  base_url=request.build_absolute_uri() ).write_pdf(response,stylesheets=[weasyprint.CSS('orders/static/css/pdf.css')], presentational_hints=True)
    return response
