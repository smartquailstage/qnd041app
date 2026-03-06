from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from .gemini_bot import responder_con_gemini
import requests

MEETING_KEYWORDS = ["cita", "reunión", "demo", "agendar"]

@csrf_exempt
def webhook_whatsapp(request):
    if request.method != "POST":
        return HttpResponse("Solo POST", status=400)

    mensaje = request.POST.get('Body')
    telefono = request.POST.get('From')

    if telefono.startswith("whatsapp:"):
        telefono = telefono.replace("whatsapp:", "")

    # Generar respuesta con Gemini
    try:
        respuesta = responder_con_gemini(mensaje, telefono)
    except Exception as e:
        respuesta = "Lo siento, estamos teniendo problemas con el sistema de asistencia. Intenta más tarde."
        print(f"Error Gemini: {e}")

    # Detectar solicitud de cita
    if any(word in mensaje.lower() for word in MEETING_KEYWORDS):
        n8n_webhook_url = "https://n8n.smartquail.io/webhook/695999b0-e680-4531-8082-37f65eaeee91"
        payload = {"telefono": telefono, "mensaje": mensaje, "respuesta": respuesta}
        try:
            requests.post(n8n_webhook_url, json=payload, timeout=5)
        except Exception as e:
            print(f"Error enviando a n8n: {e}")

    # Responder al usuario por WhatsApp
    twilio_resp = MessagingResponse()
    twilio_resp.message(respuesta)
    return HttpResponse(str(twilio_resp), content_type='text/xml')