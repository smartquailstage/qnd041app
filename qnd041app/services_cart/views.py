from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from business_customer_projects.models import PaymentOrder
from .cart import Cart
from .forms import CartAddProductForm
from services_coupons.forms import CouponApplyForm

from django.contrib.auth.decorators import login_required




from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from business_customer_projects.models import PaymentOrder
from .cart import Cart


@login_required
@require_POST
def cart_add_payment_order(request, order_id):
    cart = Cart(request)

    payment_order = get_object_or_404(
        PaymentOrder,
        id=order_id,
        user=request.user,
        pago_verificado=False
    )

    # Siempre 1, siempre override
    cart.add(
        payment_order=payment_order,
        quantity=1,
        update_quantity=True
    )

    return redirect('services_cart:cart_detail')


@login_required
def cart_remove_payment_order(request, order_id):
    cart = Cart(request)

    payment_order = get_object_or_404(
        PaymentOrder,
        id=order_id,
        user=request.user
    )

    cart.remove(payment_order)
    return redirect('services_cart:cart_detail')





@login_required
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(PaymentOrder, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('services_cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(PaymentOrder, id=product_id)
    cart.remove(product)
    return redirect('services_cart:cart_detail')


from django.contrib.messages import get_messages

from services_coupons.models import Coupon
from services_coupons.forms import CouponApplyForm


def cart_detail(request):
    cart = Cart(request)
    message = ""

    # Agregar PaymentOrders del usuario
    payments = PaymentOrder.objects.filter(user=request.user, pago_verificado=False)
    

    if request.method == 'POST':
        coupon_apply_form = CouponApplyForm(request.POST)
        if coupon_apply_form.is_valid():
            coupon_code = coupon_apply_form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True)
                request.session['coupon_id'] = coupon.id
                cart.coupon = coupon
                cart.save()
                message = "¡Cupón aplicado exitosamente!"
            except Coupon.DoesNotExist:
                message = "El cupón no es válido."
        else:
            message = "Formulario no válido."
    else:
        coupon_apply_form = CouponApplyForm()

    total = float(cart.get_total_price())
    discount = float(cart.get_discount())
    total_after_discount = float(cart.get_total_price_after_discount())

    return render(request, 'services_cart/detail.html', {
        'cart': cart,
        'total': total,
        'discount': discount,
        'total_after_discount': total_after_discount,
        'coupon_apply_form': coupon_apply_form,
        'message': message,
        'payments': payments,  # <-- PASAMOS LOS PAYMENTORDERS
    })

