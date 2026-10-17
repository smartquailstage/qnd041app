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




import requests
from datetime import timedelta
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from .models import InstagramPost

@shared_task
def publish_scheduled_instagram_posts():
    """
    Celery Beat ejecuta esta tarea cada minuto. 
    Busca posts programados y dispara un Webhook hacia n8n para su publicación.
    """
    now = timezone.now()
    
    # 1. Buscar posts cuya fecha programada ya se cumplió
    scheduled_posts = InstagramPost.objects.filter(
        status='scheduled',
        scheduled_date__lte=now
    )

    for post in scheduled_posts:
        try:
            # Bloqueamos el estado temporalmente para evitar duplicidad
            post.status = 'processing'
            post.save(update_fields=['status'])

            # 2. Obtener la URL del webhook de n8n desde la configuración
            webhook_url = settings.N8N_WEBHOOKS_A.get("instagram_post")
            
            if not webhook_url:
                raise ValueError("No se encontró la URL del webhook 'instagram_post' en N8N_WEBHOOKS_A")

            # 3. Preparar el paquete de datos (Payload) para n8n con todos los campos del modelo
            payload = {
                "post_id": post.id,
                "model": "InstagramPost",
                "status": post.status,
                "scheduled_date": post.scheduled_date.isoformat() if post.scheduled_date else None,
                
                # Relación con la cuenta de Instagram
                "account": {
                    "id": post.account.id if post.account else None,
                    "account_id": post.account.account_id if post.account else None,
                    "account_name": post.account.account_name if post.account else None,
                } if post.account else None,
                
                "image_size": post.image_size,
                
                # Relación con la categoría
                "category": {
                    "id": post.categories.id if post.categories else None,
                    "name": post.categories.name if post.categories else None,
                } if post.categories else None,
                
                "caption": post.caption,
                "copy": post.copy,
                "hashtags": post.hashtags,
                
                # URL absoluta de la imagen de Wagtail
                "image_url": post.image.file.url if post.image else None,
                
                # Datos de control
                "created_by": post.created_by.username if post.created_by else None,
                "created_at": post.created_at.isoformat() if post.created_at else None,
            }

            # 4. Disparar el Webhook POST hacia n8n
            response = requests.post(webhook_url, json=payload, timeout=30)

            # 5. Evaluar respuesta de n8n
            if response.status_code in [200, 201]:
                post.status = 'sent'
            else:
                post.status = 'failed'
                print(f"n8n rechazó el post {post.id}. Código: {response.status_code} - Respuesta: {response.text}")

            post.save(update_fields=['status'])

        except Exception as exc:
            # Si hay error de red o timeout, marcamos como fallido para auditoría
            post.status = 'failed'
            post.save(update_fields=['status'])
            print(f"Error crítico enviando webhook a n8n para el post ID {post.id}: {exc}")

    return "Proceso de publicación por Webhook completado."