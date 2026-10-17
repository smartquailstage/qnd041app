import requests
from celery import shared_task
from django.conf import settings

from social_media_A.models import (
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
    url = settings.N8N_WEBHOOKS_A.get(webhook_key)

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


# =========================
# INSTAGRAM POST
# =========================
@shared_task(bind=True, max_retries=3)
def task_instagram_post(self, payload):
    try:
        obj = mark_processing(InstagramPost, payload["id"])

        response = send_to_n8n("instagram_post", payload)

        obj.status = "sent"
        obj.save(update_fields=["status"])

        return response

    except Exception as exc:
        if obj:
            mark_failed(obj)
        raise self.retry(exc=exc)


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



from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from .models import InstagramPost  # O importa los demás modelos si deseas unificarlos

@shared_task
def publish_scheduled_instagram_posts():
    """
    Tarea periódica que revisa cada minuto los posts de Instagram programados
    cuya fecha de publicación ya haya llegado o pasado, y los procesa para su envío.
    """
    now = timezone.now()
    
    # 1. Buscar posts programados cuya fecha sea menor o igual a la actual
    scheduled_posts = InstagramPost.objects.filter(
        status='scheduled',
        scheduled_date__lte=now
    )

    published_count = 0

    for post in scheduled_posts:
        try:
            # Cambiamos a 'processing' para evitar que otra ejecución los tome simultáneamente
            post.status = 'processing'
            post.save(update_fields=['status'])

            # ==========================================
            # 🚀 AQUÍ INTEGRAS TU LÓGICA DE PUBLICACIÓN REAL
            # (Ej: Llamada a la API de Meta/Instagram Graph API, 
            # o disparar un webhook hacia n8n para que ejecute el posteo)
            # ==========================================
            
            # Simulación de envío exitoso:
            # response = enviar_a_instagram_api(post)
            
            # Si el envío es exitoso, marcamos como 'sent' (enviado)
            post.status = 'sent'
            post.save(update_fields=['status'])
            published_count += 1

        except Exception as exc:
            # Si ocurre un fallo, marcamos el post como 'failed' para auditoría
            post.status = 'failed'
            post.save(update_fields=['status'])
            print(f"Error publicando post ID {post.id}: {exc}")

    return f"Se procesaron y publicaron {published_count} posts programados de Instagram."