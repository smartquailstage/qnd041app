import requests
from celery import shared_task
from django.conf import settings
from .models import SocialAutomationPost


from celery import shared_task
from core.models import SocialAutomationPost
import requests
from django.conf import settings

import requests
from celery import shared_task
from django.conf import settings
from .models import SocialAutomationPost




@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def send_post_to_n8n(self, post_id):
    post = SocialAutomationPost.objects.get(id=post_id)

    # Idempotencia
    if post.status not in ["pending", "error"]:
        return "Already processed"

    payload = {
        "id": post.id,
        "title": post.title or post.prompt[:50],
        "prompt": post.prompt,
        "brand_voice": post.brand_voice,
        "brand_text": post.brand_text,
        "logo": post.logo_url,  # ✅ URL HTTPS del bucket
        "reference_image": post.reference_image_url,  # ✅ URL HTTPS
        "platform": "both",
        "go_live_at": post.scheduled_datetime.isoformat() if post.scheduled_datetime else None,
        "secret": settings.N8N_SECRET,
    }

    try:
        response = requests.post(
            settings.N8N_WEBHOOK_URL,
            json=payload,
            timeout=15
        )

        if response.status_code == 200:
            post.status = "processing"
        else:
            post.status = "error"

        post.save()

    except Exception as exc:
        post.status = "error"
        post.save()
        raise self.retry(exc=exc)


import requests
from celery import shared_task
from django.conf import settings
from core.models import GeneratedSocialAsset


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def send_asset_to_n8n(self, asset_id):
    try:
        asset = GeneratedSocialAsset.objects.select_related(
            "social_post", "image", "logo", "reference_image"
        ).get(id=asset_id)

        # Idempotencia
        if asset.status not in ["generated", "error"]:
            return "Already processed"

        if not settings.N8N_PUBLISH_WEBHOOK_URL:
            raise Exception("N8N_PUBLISH_WEBHOOK_URL not configured")

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
            settings.N8N_META_WEBHOOK_URL,
            json=payload,
            timeout=20
        )

        if response.status_code == 200:
            asset.status = "sent_to_n8n"
            asset.save(update_fields=["status"])
            return "Sent successfully"

        raise Exception(f"Bad response: {response.text}")

    except Exception as exc:
        asset.status = "error"
        asset.save(update_fields=["status"])
        raise self.retry(exc=exc)