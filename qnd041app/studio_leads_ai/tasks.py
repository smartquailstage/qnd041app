import requests

from celery import shared_task
from django.conf import settings

from .models import Conversation, Message



@shared_task(bind=True, max_retries=3)
def process_user_message(self, conversation_id, message_id):

    try:

        conversation = Conversation.objects.get(id=conversation_id)
        message = Message.objects.get(id=message_id)

        # historial últimos mensajes
        history = conversation.messages.order_by("-timestamp")[:5]

        history_payload = []

        for msg in reversed(history):
            history_payload.append({
                "role": msg.role,
                "content": msg.content
            })

        payload = {
            "conversation_id": conversation.id,
            "message_id": message.id,
            "username": conversation.username,
            "phone": conversation.phone,
            "message": message.content,
            "history": history_payload,
            "interaction_type": conversation.interaction_type,
            "sentiment": conversation.sentiment,
        }

        response = requests.post(
            settings.TWILIO_AUTH_TOKEN,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)


        