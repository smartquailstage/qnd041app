from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message
from .tasks import process_user_message


@receiver(post_save, sender=Message)
def message_created(sender, instance, created, **kwargs):

    if not created:
        return

    # solo mensajes usuario
    if instance.role != "user":
        return

    process_user_message.delay(
        conversation_id=instance.conversation.id,
        message_id=instance.id
    )