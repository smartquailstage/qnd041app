from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages  # Para agregar mensajes
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm

from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import CouponApplyForm
from .models import Coupon



@login_required
@require_POST
def coupon_apply(request):

    now = timezone.now()

    form = CouponApplyForm(request.POST)

    if form.is_valid():

        code = form.cleaned_data['code']

        try:
            coupon = Coupon.objects.get(
                user=request.user,
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
            )

            # Guardar cupón en sesión
            request.session['coupon_id'] = coupon.id

            messages.success(
                request,
                f"Cupón '{coupon.code}' aplicado correctamente."
            )

        except Coupon.DoesNotExist:

            # Limpiar cupón inválido
            request.session['coupon_id'] = None

            messages.error(
                request,
                "El cupón es inválido, expiró o no pertenece a esta cuenta."
            )

    else:

        messages.error(
            request,
            "Formulario inválido."
        )

    return redirect('paas_cart:cart_detail')






# views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CouponRequestForm



# views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CouponRequestForm


@login_required
def create_coupon_request(request):

    if request.method == 'POST':

        form = CouponRequestForm(request.POST)

        if form.is_valid():

            coupon = form.save(commit=False)

            # ==========================
            # ASIGNAR USUARIO
            # ==========================

            coupon.user = request.user

            # ==========================
            # VALIDACIÓN MANUAL
            # ==========================

            coupon.active = False

            # No generar código todavía
            coupon.code = None

            coupon.save()

            messages.success(
                request,
                'La solicitud fue enviada correctamente y será validada manualmente.'
            )

            return redirect('saas_shop:product_list')

    else:

        form = CouponRequestForm()

    return render(
        request,
        'create_coupon_request.html',
        {
            'form': form
        }
    )