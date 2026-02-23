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
    if data.get("secret") != settings.N8N_SECRET:
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