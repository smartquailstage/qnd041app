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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import SocialAutomationPost
from wagtail.images import get_image_model
from django.core.files.base import ContentFile

from PIL import Image as PILImage
from io import BytesIO
import requests


@api_view(['POST'])
@permission_classes([AllowAny])
def update_generated_image(request):
    try:
        data = request.data
        post = SocialAutomationPost.objects.get(id=data["id"])
        image_url = data["generated_image_url"]

        # 1️⃣ Descargar imagen generada
        r = requests.get(image_url)
        if r.status_code != 200:
            return Response(
                {"success": False, "message": "No se pudo descargar la imagen"},
                status=400
            )

        base_image = PILImage.open(BytesIO(r.content)).convert("RGBA")

        # 2️⃣ Si existe logo, superponerlo intacto
        if post.company_logo:
            logo_response = requests.get(post.company_logo.url)
            if logo_response.status_code == 200:
                logo = PILImage.open(BytesIO(logo_response.content)).convert("RGBA")

                base_width, base_height = base_image.size
                logo_width, logo_height = logo.size

                # Escalar proporcionalmente SOLO si es muy grande
                max_logo_width = int(base_width * 0.20)

                if logo_width > max_logo_width:
                    ratio = max_logo_width / logo_width
                    new_size = (
                        int(logo_width * ratio),
                        int(logo_height * ratio),
                    )
                    logo = logo.resize(new_size, PILImage.LANCZOS)

                logo_width, logo_height = logo.size

                # Posición: esquina inferior derecha
                margin = 40
                x = base_width - logo_width - margin
                y = base_height - logo_height - margin

                # Pegar respetando transparencia (NO altera el logo)
                base_image.paste(logo, (x, y), logo)

        # 3️⃣ Guardar imagen final en memoria
        buffer = BytesIO()
        base_image.save(buffer, format="PNG")
        buffer.seek(0)

        # 4️⃣ Crear imagen en Wagtail
        ImageModel = get_image_model()
        wagtail_image = ImageModel(
            title=f"Post {post.id} final image",
            file=ContentFile(buffer.read(), name=f"post_{post.id}.png")
        )
        wagtail_image.save()

        # 5️⃣ Actualizar modelo
        post.generated_image_url = wagtail_image.file.url
        post.status = data.get("status", "completed")
        post.save()

        return Response({
            "success": True,
            "message": "Imagen guardada en Wagtail con logo aplicado correctamente"
        })

    except SocialAutomationPost.DoesNotExist:
        return Response(
            {"success": False, "message": "Post no encontrado"},
            status=404
        )

    except Exception as e:
        return Response(
            {"success": False, "message": str(e)},
            status=500
        )
