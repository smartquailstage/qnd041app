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
    profile = user.profile
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
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
                SaaSOrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            cart.clear()

            order_created.delay(order.id)

            request.session['order_id'] = order.id

            # 👉 Redirige al detalle de la orden
            return redirect('saas_orders:order_detail', order_id=order.id)

        else:
            print("Formulario no válido")
            print(form.errors)
    else:
        form = OrderCreateForm()

    return render(request, 'saas_orders/order/create.html', {
        'cart': cart, 'form': form
    })




@login_required
def order_detail(request, order_id):
    order = get_object_or_404(SaaSOrder, id=order_id, user=request.user)

    return render(request, 'saas_orders/order/detail.html', {
        'order': order
    })




@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(SaaSOrder, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(SaaSOrder, id=order_id)
    html = render_to_string('saas_orders/order/pdf2.html', {'order': order})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf"'

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('saas_orders/static/css/pdf.css')],
        presentational_hints=True
    )

    return response
