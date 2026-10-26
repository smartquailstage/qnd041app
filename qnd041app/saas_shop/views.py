from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from saas_cart.forms import CartAddProductForm
from .recommender import Recommender
from django.contrib.auth.decorators import login_required
from usuarios.models import Profile   # <-- IMPORTANTE


@login_required
def product_list(request, category_slug=None):
    # Obtener el perfil del usuario
    profile = Profile.objects.get(user=request.user)

    # Filtrar categorías según tamaño de empresa del perfil
    categories = Category.objects.filter(
        tamano_empresa=profile.tamano_empresa
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
        'saas_shop/product/list.html',
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
                  'saas_shop/product/detail.html',
                  {
                      'product': product,
                      'cart_product_form': cart_product_form,
                      'recommended_products': recommended_products
                  })


import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .services import consultar_ollama_productos  # Asegúrate de importar tu servicio

@login_required
@require_POST
def ai_assistant_chat_view(request):
    """
    Vista que procesa la pregunta del usuario consultando de forma estricta 
    la base de datos a través de Ollama.
    """
    try:
        # Intentar parsear el cuerpo JSON de la petición
        data = json.loads(request.body)
        pregunta = data.get('pregunta', '').strip()
        
        if not pregunta:
            return JsonResponse({'error': 'La pregunta no puede estar vacía.'}, status=400)
        
        # Llamamos al servicio de Ollama con el contexto de la base de datos
        respuesta_ia = consultar_ollama_productos(pregunta)
        
        return JsonResponse({
            'status': 'success',
            'respuesta': respuesta_ia
        }, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Formato JSON inválido en la solicitud.'}, status=400)
        
    except Exception as e:
        # Captura cualquier otro error imprevisto del servicio o base de datos
        return JsonResponse({'error': f'Error interno del servidor: {str(e)}'}, status=500)