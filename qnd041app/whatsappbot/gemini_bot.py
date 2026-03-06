import google.generativeai as genai
from django.conf import settings
from .models import Conversacion

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

PROMPT_INICIAL = """
Eres un asistente virtual para la empresa "SmartQuail,Inc", una compañía que ofrece servicios de desarrollo web, soporte técnico y soluciones en la nube para pequeñas y medianas empresas.

🕒 Horarios de atención: Lunes a Viernes de 9:00 a 18:00.
📍 Ubicación: Bogotá, Colombia.
📞 Contacto: contacto@techsoluciones.com

Responde siempre de forma profesional, clara y en español.
"""

def responder_con_gemini(mensaje_usuario, telefono):

    historial = Conversacion.objects.filter(
        telefono=telefono
    ).order_by("-timestamp")[:6]

    historial = reversed(historial)

    contexto = []

    for c in historial:
        contexto.append(f"Usuario: {c.mensaje_usuario}")
        contexto.append(f"Asistente: {c.respuesta_bot}")

    contexto.append(f"Usuario: {mensaje_usuario}")

    prompt_final = PROMPT_INICIAL + "\n\n" + "\n".join(contexto)

    respuesta = model.generate_content(prompt_final)

    return respuesta.text