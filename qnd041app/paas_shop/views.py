from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from paas_cart.forms import CartAddProductForm
from .recommender import Recommender
from django.contrib.auth.decorators import login_required
from usuarios.models import Profile   # <-- IMPORTANTE


@login_required
def product_list(request, category_slug=None):
    profile = get_object_or_404(Profile, user=request.user)

    # 🔥 Categorías del usuario (optimizado con productos precargados)
    categories = Category.objects.filter(
        sector=profile.sector_negocio
    ).prefetch_related("products")

    # 🔥 Mapa rápido slug → categoría
    category_map = {c.slug: c for c in categories}

    # Productos base
    products = Product.objects.filter(available=True)

    category = None

    if category_slug:
        category = category_map.get(category_slug)
        if not category:
            category = get_object_or_404(categories, slug=category_slug)

        products = products.filter(category=category)

    # 🔥 CONFIG CENTRAL DE TABS (SINGLE SOURCE OF TRUTH)
    TAB_CONFIG = [
        {"slug": "business-gastronomico", "tab_id": "description", "label": "Gastronómico", "icon": "bx bx-restaurant"},
        {"slug": "business-medico", "tab_id": "more-info", "label": "Médico", "icon": "bx bx-health"},
        {"slug": "business-tecnologico", "tab_id": "tags", "label": "Tecnológico", "icon": "lni lni-code-alt"},
        {"slug": "business-educar", "tab_id": "educar", "label": "Educación", "icon": "lni lni-graduation"},
        {"slug": "business-ong", "tab_id": "ong", "label": "ONG", "icon": "ion-icon people-circle-outline"},
        {"slug": "business-publico", "tab_id": "business-public", "label": "Público", "icon": "bx bx-cabinet"},
        {"slug": "business-privado", "tab_id": "business-private", "label": "Privado", "icon": "bx bx-cabinet"},
        {"slug": "business-servicios", "tab_id": "services", "label": "Servicios", "icon": "bx bx-street-view"},
        {"slug": "business-industrial", "tab_id": "industries", "label": "Industrial", "icon": "bx bx-shape-polygon"},
        {"slug": "business-investigacion", "tab_id": "research", "label": "Investigación", "icon": "bx bx-dna"},
        {"slug": "business-art", "tab_id": "art", "label": "Arte", "icon": "bx bx-palette"},
        {"slug": "business-marketing", "tab_id": "marketing", "label": "Marketing", "icon": "bx bx-broadcast"},
        {"slug": "business-admin", "tab_id": "admin", "label": "admin", "icon": "bx bx-broadcast"},
        {"slug": "business-transporte", "tab_id": "admin", "label": "transporte", "icon": "bx bx-broadcast"},
    ]

    # 🔥 Filtrar solo tabs que realmente existen en categorías del usuario
    active_tabs = [
        tab for tab in TAB_CONFIG
        if tab["slug"] in category_map
    ]

    return render(
        request,
        "paas_shop/product/list.html",
        {
            "category": category,
            "categories": categories,
            "category_map": category_map,
            "products": products,
            "profile": profile,
            "tabs": active_tabs,   # 🔥 solo los activos
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
