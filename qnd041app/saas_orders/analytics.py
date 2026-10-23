import requests
import re
from django.conf import settings

def track_ga4_license_event(request, product_name, license_type):
    measurement_id = getattr(settings, 'GA4_MEASUREMENT_ID', 'G-TU-ID')
    api_secret = getattr(settings, 'GA4_API_SECRET', 'TU-API-SECRET')
    
    # 1. Extraer el client_id de la cookie '_ga' que deja el navegador del usuario
    ga_cookie = request.COOKIES.get('_ga', '')
    client_id = 'fallback_client_id.123456' # Valor por defecto si por alguna razón no existe
    
    # El formato típico de la cookie _ga es GA1.1.XXXXXXXXXX.YYYYYYYYYY
    match = re.search(r'GA\d+\.\d+\.(\d+\.\d+)', ga_cookie)
    if match:
        client_id = match.group(1)

    # 2. Construir el payload según la especificación de GA4 Measurement Protocol
    payload = {
        "client_id": client_id,
        "events": [{
            "name": "solicitud_licencia",
            "params": {
                "product_name": product_name,
                "license_type": license_type,
                "engagement_time_msec": 100
            }
        }]
    }

    # 3. Endpoint oficial de GA4 Measurement Protocol
    url = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}"

    try:
        response = requests.post(url, json=payload, timeout=5)
        # Nota: GA4 responde con un código HTTP 204 No Content si la petición es exitosa
        return response.status_code == 204
    except requests.RequestException as e:
        # Registrar el error en logs del servidor sin romper el flujo de la licencia
        print(f"Error enviando evento a GA4: {e}")
        return False