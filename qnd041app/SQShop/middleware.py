from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import get_language

class LocaleRedirectMiddleware:
    """
    Middleware personalizado para redirigir al idioma correspondiente si no se especifica el `locale`.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        language_code = get_language()

        # Si no hay un prefijo de idioma en la URL, redirige a la versión correspondiente.
        if not request.path.startswith(f'/{language_code}/'):
            # Redirige a la misma URL pero con el prefijo de idioma.
            return HttpResponseRedirect(f'/{language_code}{request.path}')
        
        return response
