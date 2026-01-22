from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from paas_cart.forms import CartAddProductForm
from .recommender import Recommender
from django.contrib.auth.decorators import login_required
from usuarios.models import Profile   # <-- IMPORTANTE


@login_required
def product_list(request, category_slug=None):
    # Obtener el perfil del usuario
    profile = Profile.objects.get(user=request.user)

    # Filtrar categorías según tamaño de empresa del perfil
    categories = Category.objects.filter(
        sector=profile.sector_negocio
    )

    category = None

    # Filtramos los productos disponibles
    products = Product.objects.filter(available=True)

    # Si se seleccionó una categoría, la validamos contra el filtro
    if category_slug:
        category = get_object_or_404(
            categories,  # <-- solo categorías que coinciden con el perfil
            slug=category_slug
        )
        products = products.filter(category=category)

    return render(
        request,
        'paas_shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
            'profile': profile,
        }
    )



@login_required
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(request,
                  'paas_shop/product/detail.html',
                  {
                      'product': product,
                      'cart_product_form': cart_product_form,
                      'recommended_products': recommended_products
                  })
