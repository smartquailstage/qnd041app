from rest_framework.decorators import api_view
from rest_framework.response import Response
from dateparser import parse as parse_date
from .models import PendingAppointment, CompanyInfo
from .utils.n8n_webhook import send_webhook_to_n8n
import os
import genai

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse



# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

COMPANY_CONTEXT = """
Somos SmartQuail, una empresa de soluciones inteligentes en automatización, IA y software en la nube.
Nos especializamos en crear asistentes virtuales, integraciones empresariales y plataformas escalables
basadas en Kubernetes y Python/Django. Brindamos soporte en español y trabajamos con clientes en toda Latinoamérica.
"""

# Palabras clave para detectar intención de cita
APPOINTMENT_KEYWORDS = ["cita", "reunión", "agenda", "hablar con mauricio", "consultar servicios"]

@api_view(["POST"])
def chatbot_reply(request):
    user_phone = request.data.get("from", "")
    user_message_raw = request.data.get("message", "")
    user_message_lower = user_message_raw.lower()

    # Buscar o crear cita pendiente, inicializando step si no existe
    appointment, created = PendingAppointment.objects.get_or_create(phone=user_phone)
    if created or appointment.step is None:
        appointment.step = 1
        appointment.save()

    # Paso 1: detectar intención de agendar cita
    if appointment.step == 1 and any(word in user_message_lower for word in APPOINTMENT_KEYWORDS):
        appointment.step = 2
        appointment.save()
        return Response({"reply": "¡Hola! Para agendar la cita con Mauricio Silva, ¿cuál es tu nombre?"})

    # Paso 1: conversación normal con Gemini
    if appointment.step == 1:
        return Response({"reply": gemini_response(user_message_raw, user_phone)})

    # Paso 2: guardar nombre y pedir fecha
    if appointment.step == 2 and not appointment.user_name:
        appointment.user_name = user_message_raw.strip()
        appointment.step = 3
        appointment.save()
        return Response({"reply": f"Gracias {appointment.user_name}. ¿Qué fecha y hora te gustaría para la cita? (ej: 2025-11-05 10:00)"})

    # Paso 3: guardar fecha y crear cita
    if appointment.step == 3 and not appointment.desired_date:
        desired_date = parse_date(user_message_raw, languages=['es'])
        if not desired_date:
            return Response({"reply": "No pude entender la fecha 😅. Por favor ingrésala en formato YYYY-MM-DD HH:MM"})
        
        appointment.desired_date = desired_date
        appointment.save()

        # Enviar webhook a n8n
        event_info = send_webhook_to_n8n(appointment.phone, appointment.user_name, appointment.desired_date.isoformat())
        appointment.step = 4
        appointment.save()

        html_link = event_info.get("htmlLink", "No se pudo generar el enlace")
        return Response({"reply": f"¡Perfecto {appointment.user_name}! Tu cita ha sido agendada ✅ Aquí está el enlace: {html_link}"})

    # Paso 4: conversación normal con Gemini
    return Response({"reply": gemini_response(user_message_raw, user_phone)})


def gemini_response(user_message, user_phone):
    """Genera respuesta usando Gemini con contexto de la empresa"""
    context_text = "\n".join(info.content for info in CompanyInfo.objects.filter(active=True))
    prompt = f"""
Información de la empresa:
{context_text if context_text else COMPANY_CONTEXT}

Usuario ({user_phone}) dice: "{user_message}"

Tu tarea: responde de manera natural, breve y profesional.
Si el mensaje se refiere a la empresa, sus servicios o ubicación, usa la información del contexto.
"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Lo siento 😅, tuve un problema al procesar tu mensaje."


# Función helper para Gemini
def gemini_response(user_message, user_phone):
    context_text = "\n".join(info.content for info in CompanyInfo.objects.filter(active=True))
    prompt = f"""
    Información de la empresa:
    {context_text if context_text else COMPANY_CONTEXT}

    Usuario ({user_phone}) dice: "{user_message}"

    Tu tarea: responde de manera natural, breve y profesional.
    Si el mensaje se refiere a la empresa, sus servicios o ubicación, usa la información del contexto.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Lo siento 😅, tuve un problema al procesar tu mensaje."


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "POST":
        user_phone = request.POST.get("From")  # ejemplo: 'whatsapp:+5215555555555'
        user_message = request.POST.get("Body")

        reply = chatbot_reply(user_phone, user_message)  # retorna el texto para el usuario

        resp = MessagingResponse()
        resp.message(reply)
        return HttpResponse(str(resp), content_type="text/xml")
    return HttpResponse("OK")
