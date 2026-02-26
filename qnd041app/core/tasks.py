# core/tasks.py

import requests
from celery import shared_task
from django.conf import settings
from core.models import SocialAutomationPost, GeneratedSocialAsset


# --------------------------------------------------
# Task: crear imagen en Gemini desde SocialAutomationPost
# --------------------------------------------------
@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def send_post_to_n8n(self, post_id):
    try:
        post = SocialAutomationPost.objects.get(id=post_id)

        # Evitar doble envío
        if post.status not in ["pending", "error"]:
            return "Already processed"

        # Preparar URL del logo si existe
        logo_url = post.company_logo.url if post.company_logo else None

        # Payload actualizado para n8n
        payload = {
            "id": post.id,
            "title": post.title_text or post.title or "",
            "brand_voice": post.brand_voice,
            "style": post.style,
            "color_palette": post.color_palette,
            "font_style": post.font_style,
            "format": post.format,
            "title_text": post.title_text,
            "brand_text": post.brand_text,
            "company_info_text": post.company_info_text,
            "company_logo_url": logo_url,
            "scheduled_datetime": post.scheduled_datetime.isoformat() if post.scheduled_datetime else None,
            "secret": settings.N8N_SECRET,
            "generated_image_url": post.generated_image_url or None,
        }

        # Enviar POST a n8n
        response = requests.post(
            settings.N8N_WEBHOOK_URL,
            json=payload,
            timeout=15
        )

        # Actualizar estado
        if response.status_code == 200:
            post.status = "processing"
        else:
            post.status = "error"
        post.save()

    except Exception as exc:
        post.status = "error"
        post.save()
        raise self.retry(exc=exc)

# --------------------------------------------------
# Task: editar imagen en Gemini desde GeneratedSocialAsset
# --------------------------------------------------
@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def send_asset_to_n8n(self, asset_id):
    try:
        asset = GeneratedSocialAsset.objects.select_related(
            "social_post", "image", "logo", "reference_image"
        ).get(id=asset_id)

        # Evitar doble envío
        if asset.status not in ["generated", "error"]:
            return "Already processed"

        if not hasattr(settings, "N8N_EDIT_WEBHOOK_URL") or not settings.N8N_EDIT_WEBHOOK_URL:
            raise Exception("N8N_EDIT_WEBHOOK_URL not configurada")

        # Payload para n8n
        payload = {
            "asset_id": asset.id,
            "post_id": asset.social_post.id,
            "prompt": asset.social_post.prompt,
            "brand_voice": asset.social_post.brand_voice,
            "caption": asset.caption,
            "image_url": asset.image.file.url if asset.image else None,
            "logo_url": asset.logo.file.url if asset.logo else None,
            "reference_image_url": asset.reference_image.file.url if asset.reference_image else None,
            "secret": settings.N8N_SECRET,
        }

        response = requests.post(
            settings.N8N_EDIT_WEBHOOK_URL,
            json=payload,
            timeout=20
        )

        if response.status_code == 200:
            asset.status = "sent_to_n8n"
            asset.save(update_fields=["status"])
            return "Sent successfully"

        raise Exception(f"Bad response: {response.status_code} {response.text}")

    except Exception as exc:
        asset.status = "error"
        asset.save(update_fields=["status"])
        raise self.retry(exc=exc)