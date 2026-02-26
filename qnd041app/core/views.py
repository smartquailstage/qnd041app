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






from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import SocialAutomationPost

import requests
from django.core.files.base import ContentFile
from wagtail.images import get_image_model

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
@permission_classes([AllowAny])
def update_generated_image(request):
    try:
        data = request.data
        post = SocialAutomationPost.objects.get(id=data["id"])

        image_url = data["generated_image_url"]

        # 1️⃣ Descargar imagen
        response = requests.get(image_url)
        if response.status_code != 200:
            return Response({"success": False, "message": "No se pudo descargar la imagen"}, status=400)

        # 2️⃣ Crear imagen en Wagtail
        Image = get_image_model()

        image = Image(
            title=f"Post {post.id} generated image",
            file=ContentFile(response.content, name=f"post_{post.id}.jpg"),
        )

        image.save()

        # 3️⃣ Guardar referencia en tu modelo si quieres
        post.generated_image_url = image.file.url
        post.status = data.get("status", "completed")
        post.save()

        return Response({"success": True, "message": "Imagen guardada en Wagtail"})

    except SocialAutomationPost.DoesNotExist:
        return Response({"success": False, "message": "Post no encontrado"}, status=404)

    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=500)
