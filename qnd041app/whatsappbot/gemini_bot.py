# myapp/gemini_bot.py

import google.generativeai as genai
from django.conf import settings
from .models import Conversacion

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# Prompts iniciales opcionales (para darle personalidad)
PROMPT_INICIAL = """
Eres un asistente virtual para la empresa "SmartQuail,Inc", una compañía que ofrece servicios de desarrollo web, soporte técnico y soluciones en la nube para pequeñas y medianas empresas.

🕒 Horarios de atención: Lunes a Viernes de 9:00 a 18:00.
📍 Ubicación: Bogotá, Colombia.
📞 Contacto: contacto@techsoluciones.com

Responde siempre de forma profesional, clara y en español. Si el usuario pregunta por servicios, precios o soporte, responde usando la información proporcionada.
"""

def responder_con_gemini(mensaje_usuario, telefono):
    # Obtener historial reciente (últimos 5 mensajes)
    historial = Conversacion.objects.filter(telefono=telefono).order_by('-timestamp')[:5]
    historial = reversed(historial)

    # Armar el contexto para el modelo
    contexto = [f"Usuario: {c.mensaje_usuario}\nAsistente: {c.respuesta_bot}" for c in historial]
    contexto.append(f"Usuario: {mensaje_usuario}")

    prompt_final = PROMPT_INICIAL + "\n" + "\n".join(contexto)

    # Enviar a Gemini
    respuesta = model.generate_content(prompt_final)

    # Guardar la conversación
    Conversacion.objects.create(
        telefono=telefono,
        mensaje_usuario=mensaje_usuario,
        respuesta_bot=respuesta.text
    )

    return respuesta.text
