from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from saas_shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from saas_coupons.forms import CouponApplyForm

from django.contrib.auth.decorators import login_required





@login_required
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('saas_cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('saas_cart:cart_detail')


from django.contrib.messages import get_messages

from saas_coupons.models import Coupon
from saas_coupons.forms import CouponApplyForm


def cart_detail(request):
    cart = Cart(request)
    message = ""  # Mensaje para mostrar en el template

    if request.method == 'POST':
        coupon_apply_form = CouponApplyForm(request.POST)
        if coupon_apply_form.is_valid():
            coupon_code = coupon_apply_form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True)
                # Guardamos el cupón en la sesión para que Cart lo pueda cargar
                request.session['coupon_id'] = coupon.id
                cart.coupon = coupon
                cart.save()
                message = "¡Convenio aplicado exitosamente!"
            except Coupon.DoesNotExist:
                message = "El código no es válido."
        else:
            message = "Formulario no válido."
    else:
        coupon_apply_form = CouponApplyForm()

    total = float(cart.get_total_price())
    discount = float(cart.get_discount())
    total_after_discount = float(cart.get_total_price_after_discount())

    return render(request, 'saas_cart/detail.html', {
        'cart': cart,
        'total': total,
        'discount': discount,
        'total_after_discount': total_after_discount,
        'coupon_apply_form': coupon_apply_form,
        'message': message,
    })
