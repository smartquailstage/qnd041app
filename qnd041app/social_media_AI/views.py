import requests
import json
from io import BytesIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import InstagramPost, InstagramReel, FacebookImagePost
import json
from django.core.files.base import ContentFile
from django.http import JsonResponse
from wagtail.images import get_image_model
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny







@api_view(["POST"])
@permission_classes([AllowAny])
def save_generated_image_to_wagtail(request):

    try:
        # =========================
        # 1. Obtener datos (DRF way)
        # =========================
        data = request.data  # ✔ CORRECTO EN DRF

        post_id = data.get("id")
        image_url = data.get("image")

        if not post_id or not image_url:
            return JsonResponse({"error": "Missing data"}, status=400)

        # =========================
        # 2. Obtener post
        # =========================
        post = InstagramPost.objects.get(id=post_id)

        # =========================
        # 3. Descargar imagen IA
        # =========================
        r = requests.get(image_url, timeout=30)
        r.raise_for_status()

        image_file = ContentFile(r.content)

        # =========================
        # 4. Crear imagen en Wagtail
        # =========================
        ImageModel = get_image_model()

        wagtail_image = ImageModel.objects.create(
            title=f"Instagram Post {post_id} AI Image",
            file=image_file
        )

        # =========================
        # 5. Relacionar con post
        # =========================
        post.image = wagtail_image
        post.generated_image_url = wagtail_image.file.url
        post.status = "completed"
        post.save()

        return JsonResponse({
            "success": True,
            "image_id": wagtail_image.id,
            "message": "Image saved in Wagtail"
        })

    except InstagramPost.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Image download failed: {str(e)}"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@api_view(["POST"])
@permission_classes([AllowAny])
def n8n_instagram_webhook(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)

        post_id = data.get("id")

        obj = InstagramPost.objects.get(id=post_id)

        # =========================
        # Guardar respuesta IA
        # =========================
        obj.caption = data.get("caption")
        obj.copy = data.get("copy")
        obj.hashtags = data.get("hashtags")

        image_url = data.get("image")
        if image_url:
            obj.image = image_url

        obj.status = "sent"
        obj.updated_at = timezone.now()
        obj.save()

        return JsonResponse({"status": "updated"})

    except InstagramPost.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


MODEL_MAP = {
    "InstagramPost": InstagramPost,
    "InstagramReel": InstagramReel,
    "FacebookImagePost": FacebookImagePost,
}



@api_view(["POST"])
@permission_classes([AllowAny])
def n8n_webhook_callback(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    data = json.loads(request.body)

    model_name = data.get("model")
    object_id = data.get("id")
    status = data.get("status")  # sent | failed
    message = data.get("message", "")

    model = MODEL_MAP.get(model_name)

    if not model:
        return JsonResponse({"error": "Invalid model"}, status=400)

    try:
        obj = model.objects.get(id=object_id)

        obj.status = status
        obj.updated_at = timezone.now()
        obj.save(update_fields=["status", "updated_at"])

        return JsonResponse({"ok": True})

    except model.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)