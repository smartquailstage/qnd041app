# myapp/views.py

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from .gemini_bot import responder_con_gemini

@csrf_exempt
def webhook_whatsapp(request):
    if request.method == "POST":
        mensaje = request.POST.get('Body')
        telefono = request.POST.get('From')  # Ej: "whatsapp:+521234567890"

        if telefono.startswith("whatsapp:"):
            telefono = telefono.replace("whatsapp:", "")

        respuesta = responder_con_gemini(mensaje, telefono)

        twilio_resp = MessagingResponse()
        twilio_resp.message(respuesta)
        return HttpResponse(str(twilio_resp), content_type='text/xml')

    return HttpResponse("Solo POST", status=400)
