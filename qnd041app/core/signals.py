# core/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import requests

from core.models import SocialAutomationPost, GeneratedSocialAsset, SocialPostSchedule
from core.tasks import send_post_to_n8n, send_asset_to_n8n


# 1️⃣ Signal para crear imagen desde SocialAutomationPost
@receiver(post_save, sender=SocialAutomationPost)
def trigger_n8n_on_post_save(sender, instance, created, **kwargs):
    """
    Dispara la tarea de creación de imagen en n8n
    cuando se crea un SocialAutomationPost nuevo o está pendiente.
    """
    if created or instance.status == "pending":
        send_post_to_n8n.delay(instance.id)


# 2️⃣ Signal para editar imagen desde GeneratedSocialAsset
@receiver(post_save, sender=GeneratedSocialAsset)
def trigger_n8n_on_asset_save(sender, instance, created, **kwargs):
    """
    Dispara la tarea de edición en n8n cuando un GeneratedSocialAsset
    está en estado 'generated'.
    """
    if instance.status == "generated":
        send_asset_to_n8n.delay(instance.id)


# 3️⃣ Signal para enviar al nodo de Meta (opcional, solo si usas SocialPostSchedule)
@receiver(post_save, sender=SocialPostSchedule)
def send_to_meta(sender, instance, created, **kwargs):
    """
    Envia automáticamente el post programado a Meta vía webhook.
    """
    if created and instance.status == "pending":
        payload = {
            "id": instance.id,
            "image_url": instance.image.image.file.url,
            "caption": instance.caption,
            "platform": instance.platform,
            "scheduled_datetime": instance.scheduled_datetime.isoformat(),
            "secret": settings.N8N_META_SECRET,
        }
        try:
            requests.post(settings.N8N_META_WEBHOOK_URL, json=payload, timeout=10)
            instance.status = "scheduled"
            instance.save(update_fields=["status"])
        except Exception as e:
            instance.status = "error"
            instance.save(update_fields=["status"])