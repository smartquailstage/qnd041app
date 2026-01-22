from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages  # Para agregar mensajes
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            # Si el cupón es válido, lo guardamos en la sesión
            request.session['coupon_id'] = coupon.id
            messages.success(request, f"Cupón '{coupon.code}' aplicado correctamente.")
        except Coupon.DoesNotExist:
            # Si el cupón no es válido, eliminamos cualquier cupón previo
            request.session['coupon_id'] = None
            messages.error(request, "El código del cupón es inválido o ha expirado.")
    
    return redirect('paas_cart:cart_detail')