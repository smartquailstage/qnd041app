from twilio.rest import Client
from django.conf import settings

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to, message):
    """
    to: número del cliente, ej. whatsapp:+5215555555555
    message: texto a enviar
    """
    client.messages.create(
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        body=message,
        to=to
    )