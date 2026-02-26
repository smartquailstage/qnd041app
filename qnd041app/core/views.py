# core/views.py

import json
import requests
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from wagtail.images import get_image_model

from core.models import SocialAutomationPost, GeneratedSocialAsset


# core/views.py

import json
import requests
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from wagtail.images import get_image_model
from rest_framework.decorators import api_view
from rest_framework.response import response
from core.models import SocialAutomationPost, GeneratedSocialAsset


@csrf_exempt
def social_callback(request):
    data = json.loads(request.body)

    # Seguridad
    if data.get("secret") != settings.N8N_GEMINI_SECRET:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    try:
        post = SocialAutomationPost.objects.get(id=data["id"])
        image_url = data.get("image_url")

        # Descargar imagen desde Gemini/Canva
        response = requests.get(image_url)
        response.raise_for_status()

        ImageModel = get_image_model()

        image = ImageModel.objects.create(
            title=f"Generated Post {post.id}",
            file=ContentFile(
                response.content,
                name=f"generated_post_{post.id}.jpg"
            ),
        )

        GeneratedSocialAsset.objects.create(
            social_post=post,
            caption=data.get("caption"),
            image=image,
            meta_post_id=data.get("meta_post_id"),
            status=data.get("status", "generated"),
        )

        post.status = "completed"
        post.save()

        return JsonResponse({"ok": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)






# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SocialAutomationPost

@api_view(['POST'])
def update_generated_image(request):
    if request.method == "POST":
        try:
            data = request.data.get("generated_image_url")

            # 1️⃣ Buscar el post por ID
            post = SocialAutomationPost.objects.get(id=data["id"])

            # 2️⃣ Actualizar URL de la imagen y estado
            post.generated_image_url = data["generated_image_url"]
            post.status = data.get("status", "completed")
            post.save()

            return JsonResponse({"success": True, "message": "Post actualizado"})
        except SocialAutomationPost.DoesNotExist:
            return JsonResponse({"success": False, "message": "Post no encontrado"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)