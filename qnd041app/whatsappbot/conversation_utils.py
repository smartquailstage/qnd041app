from .models import Conversacion

def obtener_historial(telefono, limite=10):

    conversaciones = Conversacion.objects.filter(
        telefono=telefono
    ).order_by("-timestamp")[:limite]

    conversaciones = list(conversaciones)[::-1]

    historial = []

    for c in conversaciones:
        historial.append({
            "role": "user",
            "content": c.mensaje_usuario
        })

        historial.append({
            "role": "assistant",
            "content": c.respuesta_bot
        })

    return historial