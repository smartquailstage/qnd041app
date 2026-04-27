import os
import requests

from django.http import JsonResponse
from django.utils import timezone
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from wagtail.images import get_image_model

from .models import InstagramPost, InstagramReel, FacebookImagePost


API_KEY = os.environ.get("INSTAGRAM_POST_API_KEY", "default_api_key")


# =========================================
# 🔥 BASE VIEW (CSRF SOLO DESACTIVADO AQUÍ)
# =========================================
@method_decorator(csrf_exempt, name="dispatch")
class BaseWebhookView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def check_api_key(self, request):
        api_key = request.META.get("HTTP_X_API_KEY")

        if api_key != API_KEY:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        return None


# =========================================
# 🔥 1. GUARDAR IMAGEN
# =========================================
class SaveGeneratedImageView(BaseWebhookView):

    def post(self, request):
        error = self.check_api_key(request)
        if error:
            return error

        try:
            post_id = request.data.get("id")
            image_url = request.data.get("image")

            if not post_id or not image_url:
                return JsonResponse({"error": "Missing data"}, status=400)

            post = InstagramPost.objects.get(id=post_id)

            r = requests.get(image_url, timeout=30)
            r.raise_for_status()

            image_file = ContentFile(r.content)
            ImageModel = get_image_model()

            wagtail_image = ImageModel.objects.create(
                title=f"Instagram Post {post_id} AI Image",
                file=image_file
            )

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

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# =========================================
# 🔥 2. INSTAGRAM WEBHOOK
# =========================================
class InstagramWebhookView(BaseWebhookView):

    def post(self, request):
        error = self.check_api_key(request)
        if error:
            return error

        try:
            obj = InstagramPost.objects.get(id=request.data.get("id"))

            obj.caption = request.data.get("caption", "")
            obj.copy = request.data.get("copy", "")
            obj.hashtags = request.data.get("hashtags", "")

            if request.data.get("image"):
                obj.image = request.data.get("image")

            obj.status = "sent"
            obj.updated_at = timezone.now()
            obj.save()

            return JsonResponse({"status": "updated"})

        except InstagramPost.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)


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
        error = self.check_api_key(request)
        if error:
            return error

        try:
            model = MODEL_MAP.get(request.data.get("model"))

            if not model:
                return JsonResponse({"error": "Invalid model"}, status=400)

            obj = model.objects.get(id=request.data.get("id"))

            obj.status = request.data.get("status")
            obj.updated_at = timezone.now()
            obj.save(update_fields=["status", "updated_at"])

            return JsonResponse({"ok": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)