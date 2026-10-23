import re
import requests
from django.conf import settings

def track_ga4_license_event(request, product_name, license_type="standard"):
    """
    Envía un evento de conversión a Google Analytics 4 utilizando Measurement Protocol
    desde el backend de Django, rescatando la cookie de sesión del navegador.
    """
    measurement_id = getattr(settings, 'GA4_MEASUREMENT_ID', None)
    api_secret = getattr(settings, 'GA4_API_SECRET', None)
    
    # Si no están configuradas las credenciales, salimos silenciosamente 
    # para evitar romper el flujo en entornos de desarrollo local.
    if not measurement_id or not api_secret:
        return False

    # 1. Extraer el client_id de la cookie '_ga' que deja Google Analytics en el navegador
    ga_cookie = request.COOKIES.get('_ga', '')
    client_id = 'fallback_client_id.123456'  # ID de respaldo por si el usuario bloquea cookies
    
    # El formato típico de la cookie _ga es GA1.1.XXXXXXXXXX.YYYYYYYYYY
    match = re.search(r'GA\d+\.\d+\.(\d+\.\d+)', ga_cookie)
    if match:
        client_id = match.group(1)

    # 2. Construir el payload según la especificación oficial de GA4 Measurement Protocol
    payload = {
        "client_id": client_id,
        "events": [{
            "name": "solicitud_licencia",  # Este es el nombre que registrará GA4 como evento
            "params": {
                "product_name": str(product_name),
                "license_type": license_type,
                "engagement_time_msec": 100
            }
        }]
    }

    # 3. URL oficial del endpoint de GA4 Measurement Protocol
    url = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}"

    try:
        # Enviamos la petición POST por detrás (timeout corto para no bloquear la web)
        response = requests.post(url, json=payload, timeout=5)
        
        # Nota: GA4 responde con un código HTTP 204 No Content si la petición es correcta
        return response.status_code == 204
        
    except requests.RequestException as e:
        # Registramos el error en los logs del servidor sin afectar la compra del usuario
        print(f"Error enviando evento a GA4 Measurement Protocol: {e}")
        return False