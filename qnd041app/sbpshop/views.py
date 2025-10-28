from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, SBPProduct, SBPProductManual, SBPStaffItem, SBPTechnologiesItem
from sbmcart.forms import CartAddProductForm
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string

import weasyprint
from io import BytesIO


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = SBPProduct.objects.filter(available=True)
    products_staff = SBPStaffItem.objects.all()  # Esto no se usa en esta vista, lo eliminamos.
    products_tech = SBPTechnologiesItem.objects.all()  # Esto no se usa en esta vista, lo eliminamos.

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request,
                  'sbpshop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'products_staff': products_staff,
                   'products_tech':products_tech,})


def product_detail(request, id, slug):
    # Obtener el producto de la base de datos
    product = get_object_or_404(SBMProduct,
                                id=id,
                                slug=slug,
                                available=True)
    
    # Obtener los items relacionados con el staff y las tecnologías
  

    # Formulario del carrito (si se requiere)
    cart_product_form = CartAddProductForm()

    # Renderizar la plantilla con los datos del producto y los items relacionados
    return render(request,
                  'sbpshop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


@staff_member_required
def admin_product_manual_pdf(request, manual_id):
    manual = get_object_or_404(SBMProductManual, id=manual_id)
    html = render_to_string('sbpshop/product/manual_pdf.html',
                            {'manual': manual})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=manual_{}.pdf"'.format(manual.id)
    weasyprint.HTML(string=html,  base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[weasyprint.CSS('sbmshop/static/css/manual_pdf.css')], presentational_hints=True)
    return response
