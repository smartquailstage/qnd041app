import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from social_media_AI.models import (
    InstagramPost,
    InstagramCarouselPost,
    InstagramReel,
    FacebookImagePost,
    FacebookVideoPost,
    FacebookCarouselPost,
    TwitterPost,
    LinkedInPost,
)


# =========================
# BASE SENDER
# =========================
def send_to_n8n(webhook_key, payload):
    url = settings.N8N_WEBHOOKS_AI.get(webhook_key)

    if not url:
        raise Exception(f"No webhook configured for {webhook_key}")

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()

    return response.text


# =========================
# HELPERS
# =========================
def mark_processing(model, obj_id):
    try:
        obj = model.objects.get(id=obj_id)
        obj.status = "processing"
        obj.save(update_fields=["status"])
        return obj
    except model.DoesNotExist:
        return None


def mark_failed(obj):
    try:
        obj.status = "failed"
        obj.save(update_fields=["status"])
    except Exception:
        pass



@shared_task(bind=True, max_retries=3)
def task_instagram_post(self, payload):
    obj = None

    try:
        # =========================
        # 1. Obtener objeto
        # =========================
        obj = mark_processing(InstagramPost, payload["id"])

        # =========================
        # 2. Enviar a n8n (IA GENERA TODO)
        # =========================
        response = send_to_n8n("instagram_post", {
            "id": obj.id,
            "prompt": obj.prompt,
            "categories": obj.categories.id if obj.categories else None,
        })

        # =========================
        # 3. RECIBIR RESPUESTA IA
        # =========================
        obj.caption = response.get("caption")
        obj.copy = response.get("copy")
        obj.hashtags = response.get("hashtags")

        # Imagen generada (URL desde Gemini / n8n)
        image_url = response.get("image_url")
        if image_url:
            obj.image = image_url

        # =========================
        # 4. Guardar en Wagtail
        # =========================
        obj.status = "sent"
        obj.updated_at = timezone.now()
        obj.save()

        return response

    except Exception as exc:
        if obj:
            mark_failed(obj)

        raise self.retry(exc=exc, countdown=10 ** self.request.retries)

# =========================
# INSTAGRAM CAROUSEL
# =========================
@shared_task(bind=True, max_retries=3)
def task_instagram_carousel(self, payload):
    try:
        obj = mark_processing(InstagramCarouselPost, payload["id"])

        response = send_to_n8n("instagram_carousel", payload)

        obj.status = "sent"
        obj.save(update_fields=["status"])

        return response

    except Exception as exc:
        if obj:
            mark_failed(obj)
        raise self.retry(exc=exc)


# =========================
# INSTAGRAM REEL
# =========================
@shared_task(bind=True, max_retries=3)
def task_instagram_reel(self, payload):
    try:
        obj = mark_processing(InstagramReel, payload["id"])

        response = send_to_n8n("instagram_reel", payload)

        obj.status = "sent"
        obj.save(update_fields=["status"])

        return response

    except Exception as exc:
        if obj:
            mark_failed(obj)
        raise self.retry(exc=exc)


# =========================
# FACEBOOK IMAGE
# =========================
@shared_task(bind=True, max_retries=3)
def task_facebook_image(self, payload):
    try:
        obj = mark_processing(FacebookImagePost, payload["id"])

        response = send_to_n8n("facebook_image", payload)

        obj.status = "sent"
        obj.save(update_fields=["status"])

        return response

    except Exception as exc:
        if obj:
            mark_failed(obj)
        raise self.retry(exc=exc)


# =========================
# FACEBOOK VIDEO
# =========================
@shared_task(bind=True, max_retries=3)
def task_facebook_video(self, payload):
    try:
        obj = mark_processing(FacebookVideoPost, payload["id"])

        response = send_to_n8n("facebook_video", payload)

        obj.status = "sent"
        obj.save(update_fields=["status"])

        return response

    except Exception as exc:
        if obj:
            mark_failed(obj)
        raise self.retry(exc=exc)


# =========================
# FACEBOOK CAROUSEL
# =========================
@shared_task(bind=True, max_retries=3)
def task_facebook_carousel(self, payload):
    try:
        obj = mark_processing(FacebookCarouselPost, payload["id"])

        response = send_to_n8n("facebook_carousel", payload)

        obj.status = "sent"
        obj.save(update_fields=["status"])

        return response

    except Exception as exc:
        if obj:
            mark_failed(obj)
        raise self.retry(exc=exc)


# =========================
# TWITTER POST
# =========================
@shared_task(bind=True, max_retries=3)
def task_twitter_post(self, payload):
    try:
        obj = mark_processing(TwitterPost, payload["id"])

        response = send_to_n8n("twitter_post", payload)

        obj.status = "sent"
        obj.save(update_fields=["status"])

        return response

    except Exception as exc:
        if obj:
            mark_failed(obj)
        raise self.retry(exc=exc)


# =========================
# LINKEDIN POST
# =========================
@shared_task(bind=True, max_retries=3)
def task_linkedin_post(self, payload):
    try:
        obj = mark_processing(LinkedInPost, payload["id"])

        response = send_to_n8n("linkedin_post", payload)

        obj.status = "sent"
        obj.save(update_fields=["status"])

        return response

    except Exception as exc:
        if obj:
            mark_failed(obj)
        raise self.retry(exc=exc)