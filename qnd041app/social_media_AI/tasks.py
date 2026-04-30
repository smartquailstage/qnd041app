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

    return response.json()


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
    # Importaciones locales para evitar Circular Imports
    from .models import InstagramPost 
    obj = None

    try:
        # 0. VALIDACIÓN DE ESTADO
        check_obj = InstagramPost.objects.filter(id=payload["id"]).first()
        
        if not check_obj:
            print(f"❌ Error: El post {payload['id']} no existe.")
            return {"status": "error", "message": "Post not found"}

        if check_obj.status in ["sent", "processing"]:
            print(f"⚠️ Abortando: El post {payload['id']} ya está en estado {check_obj.status}")
            return {"status": "skipped", "message": "Already processed"}

        # 1. Marcar inicio de procesamiento
        obj = mark_processing(InstagramPost, payload["id"])

        # 2. ENVIAR A n8n (Con navegación segura para logos)
        cat = obj.categories # Alias para limpiar el código
        
        n8n_payload = {
            "id": obj.id,
            "prompt": obj.prompt,
            "categories": cat.id if cat else None,
            "campagin_name": cat.name if cat else None,
            "style": cat.style if cat else None,
            "primary_brand": cat.brand_1 if cat else None,
            "secondary_brand": cat.brand_2 if cat else None,

            # NAVEGACIÓN SEGURA PARA LOGOS:
            "logo_primary": cat.logo_1.file.url if cat and cat.logo_1 and hasattr(cat.logo_1, 'file') else None,
            "logo_secondary": cat.logo_2.file.url if cat and cat.logo_2 and hasattr(cat.logo_2, 'file') else None,
            "color_primary": cat.color_1 if cat else None,
            "color_secondary": cat.color_2 if cat else None,
            "color_palette": cat.color_palette if cat else None,

            "image_size": obj.image_size or "1080x1080", # Valor por defecto
            "copy": obj.copy or "",
            "post_type": obj.post_type or "",
            "caption": obj.caption or "",
            "hashtags": obj.hashtags or "",
            "image": obj.image or None,   
            "scheduled_date": obj.scheduled_date.isoformat() if obj.scheduled_date else None,
        }

        response = send_to_n8n("instagram_post", n8n_payload)

        # 3. RECIBIR Y VALIDAR RESPUESTA IA
        # Usamos .get() con fallback a string vacío para evitar IntegrityErrors (nulls)
        obj.caption = response.get("caption") or obj.caption or ""
        obj.copy = response.get("copy") or obj.copy or ""
        obj.hashtags = response.get("hashtags") or obj.hashtags or ""

        image_url = response.get("image") or response.get("generated_image_url")
        if image_url:
            obj.image = image_url

        # 4. GUARDAR EN WAGTAIL
        obj.status = "sent"
        obj.updated_at = timezone.now()
        # Guardamos solo los campos que cambiaron para ser más eficientes
        obj.save(update_fields=["caption", "copy", "hashtags", "image", "status", "updated_at"])

        return {"status": "success", "post_id": obj.id}

    except Exception as exc:
        print(f"💥 Error en tarea Celery: {exc}")
        if obj:
            mark_failed(obj)
        # Reintento exponencial
        raise self.retry(exc=exc, countdown=10 ** (self.request.retries + 1))
# =========================
# INSTAGRAM CAROUSEL
# =========================
@shared_task(bind=True, max_retries=3)
def task_instagram_carousel(self, payload):
    from .models import InstagramCarouselPost

    obj = None

    try:
        # 0. VALIDACIÓN
        check_obj = InstagramCarouselPost.objects.filter(id=payload["id"]).first()

        if not check_obj:
            print(f"❌ Error: El carousel {payload['id']} no existe.")
            return {"status": "error", "message": "Carousel not found"}

        if check_obj.status in ["sent", "processing"]:
            print(f"⚠️ Abortando: El carousel {payload['id']} ya está en estado {check_obj.status}")
            return {"status": "skipped", "message": "Already processed"}

        # 1. MARCAR PROCESSING
        obj = mark_processing(InstagramCarouselPost, payload["id"])

        if not obj:
            raise Exception("No se pudo marcar como processing")

        # 2. BUILD PAYLOAD DESDE DB (NO desde payload del signal)
        images_payload = []

        for item in obj.images.all():
            images_payload.append({
                "id": item.id,
                "caption": item.caption or "",
                "copy": item.copy or "",
                "hashtags": item.hashtags or "",
                "image": item.image.file.url if item.image and hasattr(item.image, "file") else None,
            })

        cat = obj.categories

        n8n_payload = {
            "id": obj.id,
            "prompt": obj.prompt,

            "categories": cat.id if cat else None,
            "campagin_name": cat.name if cat else None,
            "style": cat.style if cat else None,
            "primary_brand": cat.brand_1 if cat else None,
            "secondary_brand": cat.brand_2 if cat else None,

            "logo_primary": cat.logo_1.file.url if cat and cat.logo_1 and hasattr(cat.logo_1, 'file') else None,
            "logo_secondary": cat.logo_2.file.url if cat and cat.logo_2 and hasattr(cat.logo_2, 'file') else None,

            "color_primary": cat.color_1 if cat else None,
            "color_secondary": cat.color_2 if cat else None,
            "color_palette": cat.color_palette if cat else None,

            "images": images_payload,

            "scheduled_date": obj.scheduled_date.isoformat() if obj.scheduled_date else None,
        }

        # 3. SEND → n8n
        response = send_to_n8n("instagram_carousel", n8n_payload)

        # 4. UPDATE INLINE ITEMS
        images_response = response.get("images", [])

        for item in obj.images.all():
            res = next((img for img in images_response if img.get("id") == item.id), None)

            if not res:
                continue

            item.caption = res.get("caption") or item.caption or ""
            item.copy = res.get("copy") or item.copy or ""
            item.hashtags = res.get("hashtags") or item.hashtags or ""

            image_url = res.get("image") or res.get("generated_image_url")

            if image_url:
                # ⚠️ IMPORTANTE: esto depende de cómo manejes imágenes
                item.image = image_url  # ← si usas URLs directas OK, si usas Wagtail Image NO

            item.save(update_fields=["caption", "copy", "hashtags", "image"])

        # 5. FINALIZAR
        obj.status = "sent"
        obj.updated_at = timezone.now()
        obj.save(update_fields=["status", "updated_at"])

        return {"status": "success", "carousel_id": obj.id}

    except Exception as exc:
        print(f"💥 Error en carousel task: {exc}")

        if obj:
            mark_failed(obj)

        raise self.retry(exc=exc, countdown=10 ** (self.request.retries + 1))

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