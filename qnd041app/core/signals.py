from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import SocialAutomationPost
from core.tasks import send_post_to_n8n
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SocialPostSchedule
from django.conf import settings
import requests
import json

@receiver(post_save, sender=SocialAutomationPost)
def trigger_n8n_on_snippet_save(sender, instance, created, **kwargs):
    # Solo si es nuevo o pendiente
    if instance.status == "pending":
        send_post_to_n8n.delay(instance.id)



@receiver(post_save, sender=SocialPostSchedule)
def send_to_meta(sender, instance, created, **kwargs):
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
            instance.save()
        except Exception as e:
            instance.status = "error"
            instance.save()


from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import GeneratedSocialAsset
from core.tasks import send_asset_to_n8n


@receiver(post_save, sender=GeneratedSocialAsset)
def trigger_n8n_on_asset_save(sender, instance, created, **kwargs):
    """
    Dispara el webhook hacia n8n cuando el asset está listo
    """

    # Solo cuando está generado y no ha sido enviado
    if instance.status == "generated":
        send_asset_to_n8n.delay(instance.id)