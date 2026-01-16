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



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderCreateForm, AcceptTermsForm
from .models import SaaSOrder

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms



# views.py
@login_required
def accept_terms(request):
    if request.method == 'POST':
        form = AcceptTermsForm(request.POST)
        if form.is_valid():
            # Guardamos en sesión que aceptó los términos
            request.session['terms_accepted'] = True
            # Redirige a order_create
            return redirect('saas_orders:order_create')
    else:
        form = AcceptTermsForm()

    return render(request, 'saas_orders/accept_terms.html', {'form': form})


@login_required
def order_create(request):
    user = request.user
    cart = Cart(request)

    # Verificamos si aceptó los términos
    if not request.session.get('terms_accepted'):
        return redirect('saas_orders:accept_terms')

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
            order.telefono = user.telefono
            order.sector = user.sector_negocios
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

            # Limpiamos la sesión de términos aceptados
            del request.session['terms_accepted']

            return redirect('saas_orders:order_detail', order_id=order.id)
        else:
            print("Formulario no válido")
            print(form.errors)
    else:
        form = OrderCreateForm()

    return render(request, 'saas_orders/order/create.html', {'cart': cart, 'form': form})




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



from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
import weasyprint
from saas_orders.models import SaaSOrder

@staff_member_required
def admin_ebook_pdf(request, order_id):
    order = get_object_or_404(SaaSOrder, id=order_id)

    # Renderizamos la plantilla del eBook
    html = render_to_string('saas_orders/ebook/ebook_template.html', {'order': order, 'domain': 'ec.smartquail.io'})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=ebook_{order.id}.pdf'

    # Generamos el PDF usando WeasyPrint
    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[weasyprint.CSS('saas_orders/static/css/ebook.css')],
        presentational_hints=True
    )

    return response




import base64
import io
import qrcode
import hashlib

from django.conf import settings


@staff_member_required
def admin_contract_ip_pdf(request, order_id):
    order = get_object_or_404(SaaSOrder, id=order_id)

    # ------------------------------
    # Generar HASH IP (solo una vez)
    # ------------------------------
    if not order.contract_hash_ip:
        order.contract_hash_ip = order.generate_contract_hash_ip()
        order.save(update_fields=["contract_hash_ip"])

    # ------------------------------
    # URL de verificación
    # ------------------------------
    verification_url = (
        f"http://ec.smartquail.io/es/business_customer_projects/"
        f"verify/contract/ip/{order.contract_hash_ip}/"
    )

    qr_data = (
        "SMARTQUAIL S.A.S\n"
        "R.U.C: 1793206532-001\n"
        "UIO - Ecuador\n"
        "REPRESENTANTE LEGAL\n"
        "SANTIAGO SILVA DOMINGUEZ MAURICIO\n"
        f"CONTRATO: CPI-SQ20{order.id}\n"
        f"TOKEN: {order.contract_hash_ip}\n"
        f"Validar contrato: {verification_url}"
    )

    qr = qrcode.QRCode(version=1, box_size=1, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    qr_data_url = f"data:image/png;base64,{qr_base64}"

    html = render_to_string(
        "saas_orders/contracts/contract_ip.html",
        {
            "order": order,
            "domain": "ec.smartquail.io",
            "qr_url": qr_data_url,
            "contract_hash_ip": order.contract_hash_ip,
        }
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f"attachment; filename=contract_ip_{order.id}.pdf"
    )

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[weasyprint.CSS("saas_orders/static/css/contract_ip.css")],
        presentational_hints=True
    )

    return response


@staff_member_required
def admin_contract_development_pdf(request, order_id):
    order = get_object_or_404(SaaSOrder, id=order_id)

    # ------------------------------
    # Generar HASH DEV
    # ------------------------------
    if not order.contract_hash_dev:
        order.contract_hash_dev = order.generate_contract_hash_dev()
        order.save(update_fields=["contract_hash_dev"])

    verification_url = (
        f"http://ec.smartquail.io/es/business_customer_projects/"
        f"verify/contract/development/{order.contract_hash_dev}/"
    )

    qr_data = (
        "SMARTQUAIL S.A.S\n"
        "R.U.C: 1793206532-001\n"
        "UIO - Ecuador\n"
        "REPRESENTANTE LEGAL\n"
        "SANTIAGO SILVA DOMINGUEZ MAURICIO\n"
        f"CONTRATO: CD-SQ20{order.id}\n"
        f"TOKEN: {order.contract_hash_dev}\n"
        f"Validar contrato: {verification_url}"
    )

    qr = qrcode.QRCode(version=1, box_size=1, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    qr_data_url = f"data:image/png;base64,{qr_base64}"

    html = render_to_string(
        "saas_orders/contracts/contract_development.html",
        {
            "order": order,
            "domain": "ec.smartquail.io",
            "qr_url": qr_data_url,
            "contract_hash_dev": order.contract_hash_dev,
        }
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f"attachment; filename=contract_development_{order.id}.pdf"
    )

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[weasyprint.CSS("saas_orders/static/css/contract_dev.css")],
        presentational_hints=True
    )

    return response


@staff_member_required
def admin_contract_cloud_pdf(request, order_id):
    order = get_object_or_404(SaaSOrder, id=order_id)

    # ------------------------------
    # Generar HASH CLOUD
    # ------------------------------
    if not order.contract_hash_cloud:
        order.contract_hash_cloud = order.generate_contract_hash_cloud()
        order.save(update_fields=["contract_hash_cloud"])

    verification_url = (
        f"http://ec.smartquail.io/es/business_customer_projects/"
        f"verify/contract/cloud/{order.contract_hash_cloud}/"
    )

    qr_data = (
        "SMARTQUAIL S.A.S\n"
        "R.U.C: 1793206532-001\n"
        "UIO - Ecuador\n"
        "REPRESENTANTE LEGAL\n"
        "SANTIAGO SILVA DOMINGUEZ MAURICIO\n"
        f"CONTRATO: CC-SQ20{order.id}\n"
        f"TOKEN: {order.contract_hash_cloud}\n"
        f"Validar contrato: {verification_url}"
    )

    qr = qrcode.QRCode(version=1, box_size=1, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    qr_data_url = f"data:image/png;base64,{qr_base64}"

    html = render_to_string(
        "saas_orders/contracts/contract_cloud_rent.html",
        {
            "order": order,
            "domain": "ec.smartquail.io",
            "qr_url": qr_data_url,
            "contract_hash_cloud": order.contract_hash_cloud,
        }
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f"attachment; filename=contract_cloud_{order.id}.pdf"
    )

    weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS("saas_orders/static/css/contratct_resources.css")
        ],
        presentational_hints=True
    )

    return response
