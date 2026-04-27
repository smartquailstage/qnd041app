import requests
import os

from django.http import JsonResponse
from django.utils import timezone
from django.core.files.base import ContentFile

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from wagtail.images import get_image_model

from .models import InstagramPost, InstagramReel, FacebookImagePost



API_KEY = os.environ.get("INSTAGRAM_POST_API_KEY", "default_api_key")  # ❗ Cambia esto en producción


# =========================================
# 🔥 BASE CLASS (evita repetir código)
# =========================================
class BaseWebhookView(APIView):
    authentication_classes = []  # ❗ clave para evitar CSRF
    permission_classes = [AllowAny]

    def validate_api_key(self, request):
        if request.headers.get("X-API-KEY") != API_KEY:
            return JsonResponse({"error": "Unauthorized"}, status=403)
        return None


# =========================================
# 🔥 1. GUARDAR IMAGEN DESDE IA
# =========================================
class SaveGeneratedImageView(BaseWebhookView):

    def post(self, request):
        try:
            error = self.validate_api_key(request)
            if error:
                return error

            data = request.data

            post_id = data.get("id")
            image_url = data.get("image")

            if not post_id or not image_url:
                return JsonResponse({"error": "Missing data"}, status=400)

            post = InstagramPost.objects.get(id=post_id)

            # Descargar imagen
            r = requests.get(image_url, timeout=30)
            r.raise_for_status()

            image_file = ContentFile(r.content)

            # Guardar en Wagtail
            ImageModel = get_image_model()

            wagtail_image = ImageModel.objects.create(
                title=f"Instagram Post {post_id} AI Image",
                file=image_file
            )

            # Relacionar
            post.image = wagtail_image
            post.generated_image_url = wagtail_image.file.url
            post.status = "completed"
            post.updated_at = timezone.now()
            post.save()

            return JsonResponse({
                "success": True,
                "image_id": wagtail_image.id
            })

        except InstagramPost.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Download error: {str(e)}"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# =========================================
# 🔥 2. RESPUESTA IA
# =========================================
class InstagramWebhookView(BaseWebhookView):

    def post(self, request):
        try:
            error = self.validate_api_key(request)
            if error:
                return error

            data = request.data

            post_id = data.get("id")
            obj = InstagramPost.objects.get(id=post_id)

            obj.caption = data.get("caption")
            obj.copy = data.get("copy")
            obj.hashtags = data.get("hashtags")

            image_url = data.get("image")
            if image_url:
                obj.image = image_url  # solo si es URLField

            obj.status = "sent"
            obj.updated_at = timezone.now()
            obj.save()

            return JsonResponse({"status": "updated"})

        except InstagramPost.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# =========================================
# 🔥 3. CALLBACK GENÉRICO
# =========================================
MODEL_MAP = {
    "InstagramPost": InstagramPost,
    "InstagramReel": InstagramReel,
    "FacebookImagePost": FacebookImagePost,
}


class GenericWebhookCallbackView(BaseWebhookView):

    def post(self, request):
        try:
            error = self.validate_api_key(request)
            if error:
                return error

            data = request.data

            model_name = data.get("model")
            object_id = data.get("id")
            status = data.get("status")

            model = MODEL_MAP.get(model_name)

            if not model:
                return JsonResponse({"error": "Invalid model"}, status=400)

            obj = model.objects.get(id=object_id)

            obj.status = status
            obj.updated_at = timezone.now()
            obj.save(update_fields=["status", "updated_at"])

            return JsonResponse({"ok": True})

        except model.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)