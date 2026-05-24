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

from django.core.files.base import ContentFile



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
            "acting": cat.acting if cat else None,

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
import requests
from django.core.files.base import ContentFile
from django.utils import timezone
from celery import shared_task
from io import BytesIO
 
from wagtail.images import get_image_model
from wagtail.models import Collection


@shared_task(bind=True, max_retries=3)
def task_instagram_carousel(self, payload):

    obj = None

    try:
        # ========================================================
        # 0. VALIDACIÓN BASE
        # ========================================================
        if not payload or "id" not in payload:
            return {"status": "error", "message": "Missing payload id"}

        obj_id = payload.get("id")

        obj = InstagramCarouselPost.objects.filter(id=obj_id).first()

        if not obj:
            print(f"❌ Error: El carousel {obj_id} no existe.")
            return {"status": "error", "message": "Carousel not found", "fatal": True}

        if obj.status in ["sent", "processing"]:
            print(f"⚠️ Abortando: El carousel {obj_id} ya está en estado {obj.status}")
            return {"status": "skipped", "message": "Already processed"}

        # ========================================================
        # 1. MARCAR PROCESSING
        # ========================================================
        obj = mark_processing(InstagramCarouselPost, obj_id)

        if not obj:
            raise Exception("No se pudo marcar como processing")

        # ========================================================
        # 2. SAFE DATA
        # ========================================================
        payload_data = payload or {}
        cat = obj.categories

        def get_value(key, fallback):
            v = payload_data.get(key)
            return v if v not in [None, ""] else fallback

        images_payload = [
            {
                "id": i.id,
                "sort_order": i.sort_order,
                "caption": i.caption or "",
                "copy": i.copy or "",
                "hashtags": i.hashtags or "",
            }
            for i in obj.images.all()
        ]

        # ========================================================
        # 🎨 N8N PAYLOAD (FULL DJANGO CONSISTENT)
        # ========================================================
        n8n_payload = {
            # CORE
            "id": obj.id,
            "prompt": obj.prompt,
            "slides_count": obj.slides,

            # CAMPAIGN (CategoryItem)
            "campaign_name": getattr(cat, "name", "General"),

            # STYLE (CategoryItem.style)
            "style": get_value("style", getattr(cat, "style", "futuristic")),

            # BRAND (CategoryItem)
            "primary_brand": getattr(cat, "brand_1", "SmartQuail"),

            # LOGOS (CategoryItem)
            "logo_primary": getattr(cat, "image_url_1", None),
            "logo_secondary": getattr(cat, "image_url_2", None),

            # COLORS (CategoryItem + override payload)
            "color_primary": get_value(
                "color_primary",
                getattr(cat, "color_1", "#00FFFF")
            ),

            "color_secondary": get_value(
                "color_secondary",
                getattr(cat, "color_2", "#FFFFFF")
            ),

            "color_palette": get_value(
                "color_palette",
                getattr(cat, "color_palette", "vibrant")
            ),

            # 🔥 FIX CRÍTICO QUE TE FALTABA
            "image_size": get_value(
                "image_size",
                getattr(obj, "image_size", "square")
            ),

            # SCHEDULE
            "scheduled_date": (
                obj.scheduled_date.isoformat()
                if obj.scheduled_date
                else None
            ),

            # EXISTING IMAGES
            "existing_images": images_payload,
        }

        # ========================================================
        # 3. SEND → N8N
        # ========================================================
        response = send_to_n8n("instagram_carousel", n8n_payload)

        if not response:
            raise Exception("Empty response from n8n")

        # 🔥 FIX CRÍTICO: async workflow (n8n responde esto)
        if isinstance(response, dict) and "message" in response:
            raise Exception(f"n8n async response: {response}")

        images_response = response.get("images")

        if not images_response or not isinstance(images_response, list):
            raise Exception(f"n8n invalid response: {response}")

        # ========================================================
        # 4. IMAGE PROCESSING
        # ========================================================
        ImageModel = get_image_model()

        try:
            collection = Collection.objects.get(name="Root")
        except:
            collection = Collection.get_first_root_node()

        for index, res in enumerate(images_response):

            image_url = (
                res.get("image_url")
                or res.get("image")
                or res.get("generated_image_url")
            )

            if not image_url:
                continue

            img_res = requests.get(image_url, timeout=30)
            img_res.raise_for_status()

            file_name = f"carousel_{obj.id}_slide_{index + 1}.png"

            wagtail_img = ImageModel(
                title=f"Slide {index + 1} - Carousel {obj.id}",
                collection=collection
            )

            wagtail_img.file.save(
                file_name,
                ContentFile(img_res.content),
                save=True
            )

            InstagramCarouselImage.objects.update_or_create(
                post=obj,
                sort_order=index,
                defaults={
                    "image": wagtail_img,
                    "caption": res.get("caption") or "",
                    "copy": res.get("copy") or "",
                    "hashtags": res.get("hashtags") or "",
                }
            )

        # ========================================================
        # 5. FINALIZAR
        # ========================================================
        obj.status = "sent"
        obj.updated_at = timezone.now()

        if images_response and not obj.caption:
            obj.caption = images_response[0].get("caption", "")
            obj.hashtags = images_response[0].get("hashtags", "")

        obj.save(update_fields=["status", "updated_at", "caption", "hashtags"])

        return {
            "status": "success",
            "carousel_id": obj.id,
            "slides_processed": len(images_response),
        }

    except Exception as exc:

        print(f"💥 Error en carousel task: {exc}")

        if obj:
            mark_failed(obj)

        # ========================================================
        # RETRY CONTROLADO
        # ========================================================
        if "Carousel not found" in str(exc):
            return {"status": "error", "fatal": True}

        countdown = 60 * (2 ** self.request.retries)

        raise self.retry(exc=exc, countdown=countdown)

@shared_task(bind=True, max_retries=3)
def task_instagram_reel(self, payload):
    
    obj = None

    try:
        # 0. VALIDACIÓN
        obj = InstagramReel.objects.filter(id=payload["id"]).first()
        
        if not obj:
            return {"status": "error", "message": "Reel not found"}

        if obj.status in ["sent", "processing"]:
            return {"status": "skipped", "message": "Already processed"}

        # 1. Marcar inicio
        obj = mark_processing(InstagramReel, payload["id"])

        # 2. PAYLOAD PARA n8n
        cat = obj.categories
        n8n_payload = {
            "id": obj.id,
            "prompt": obj.prompt,
            "duration": obj.duration,
            "copy": obj.copy or "",
            "caption": obj.caption or "",
            "hashtags": obj.hashtags or "",
            # Branding seguro
            "acting": cat.acting if cat else None,
            "logo_primary": cat.logo_1.file.url if cat and cat.logo_1 else None,
            "color_primary": cat.color_1 if cat else None,
        }

        # 3. ENVIAR A n8n
        response = send_to_n8n("instagram_reel", n8n_payload)

        # 4. ACTUALIZAR URL Y TEXTOS
        video_url = response.get("video_url") or response.get("generated_video_url")
        if video_url:
            obj.generated_video_url = video_url

        obj.caption = response.get("caption") or obj.caption or ""
        obj.copy = response.get("copy") or obj.copy or ""
        obj.hashtags = response.get("hashtags") or obj.hashtags or ""

        # 5. GUARDAR VIDEO EN WAGTAIL MEDIA
        if video_url:
            try:
                res = requests.get(video_url, timeout=120)
                res.raise_for_status()
                # El campo 'video' debe estar configurado para wagtailmedia
                file_name = f"reel_{obj.id}_{timezone.now().strftime('%H%M')}.mp4"
                obj.video.save(file_name, ContentFile(res.content), save=False)
            except Exception as e:
                print(f"⚠️ Fallo descarga de video: {e}")

        # 6. FINALIZAR
        obj.status = "sent"
        obj.updated_at = timezone.now()
        obj.save()

        return {"status": "success", "reel_id": obj.id}

    except Exception as exc:
        print(f"💥 Error en tarea Celery Reel: {exc}")
        # Aquí mark_failed ya estará disponible porque se importó al inicio de la función
        if obj:
            mark_failed(obj)
        
        raise self.retry(exc=exc, countdown=20)


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