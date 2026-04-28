import os
import requests
import json


from django.http import JsonResponse
from django.utils import timezone
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from wagtail.images import get_image_model

from .models import InstagramPost, InstagramReel, FacebookImagePost


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from wagtail.images import get_image_model

from .models import InstagramPost

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable
from wagtail.images import get_image_model

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtailmedia.models import Media

from .settings import CategoryItem
from wagtail.fields import RichTextField


import requests
from io import BytesIO
from PIL import Image as PILImage

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model

from wagtail.images import get_image_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import InstagramPost


User = get_user_model()
Image = get_image_model()



@api_view(['POST'])
@permission_classes([AllowAny])
def update_generated_image(request):
    try:
        data = request.data

        post_id = data.get("id")
        image_url = data.get("image")

        if not post_id or not image_url:
            return Response(
                {"success": False, "message": "id o image faltantes"},
                status=400
            )

        post = InstagramPost.objects.get(id=post_id)

        # 1️⃣ Descargar imagen
        r = requests.get(image_url, timeout=10)
        if r.status_code != 200:
            return Response(
                {"success": False, "message": "No se pudo descargar la imagen"},
                status=400
            )

        base_image = PILImage.open(BytesIO(r.content)).convert("RGBA")

        # 2️⃣ Logo
        if getattr(post.categories, "logo_1", None):
            logo_response = requests.get(post.categories.logo_1.url, timeout=10)

            if logo_response.status_code == 200:
                logo = PILImage.open(BytesIO(logo_response.content)).convert("RGBA")

                base_width, base_height = base_image.size
                logo_width, logo_height = logo.size

                max_logo_width = int(base_width * 0.20)

                if logo_width > max_logo_width:
                    ratio = max_logo_width / logo_width
                    logo = logo.resize(
                        (int(logo_width * ratio), int(logo_height * ratio)),
                        PILImage.LANCZOS
                    )

                logo_width, logo_height = logo.size

                margin = 40
                x = base_width - logo_width - margin
                y = base_height - logo_height - margin

                base_image.paste(logo, (x, y), logo)

        # 3️⃣ Guardar
        buffer = BytesIO()
        base_image.save(buffer, format="PNG")
        buffer.seek(0)

        ImageModel = get_image_model()
        wagtail_image = ImageModel(
            title=f"Post {post.id} final image",
            file=ContentFile(buffer.read(), name=f"post_{post.id}.png")
        )
        wagtail_image.save()

        # ⚠️ Ajusta según tu modelo
        post.image = wagtail_image.file.url
        post.status = data.get("status", "Procesando")
        post.save()

        return Response({
            "success": True,
            "message": "Imagen procesada correctamente"
        })

    except InstagramPost.DoesNotExist:
        return Response(
            {"success": False, "message": "Post no encontrado"},
            status=404
        )

    except Exception as e:
        return Response(
            {"success": False, "message": str(e)},
            status=500
        )



from .models import InstagramPost


@api_view(['POST'])
@permission_classes([AllowAny])
def instagram_webhook(request):

    data = request.data

    try:
        post = InstagramPost.objects.get(id=data.get("id"))

        post.caption = data.get("caption", "")
        post.copy = data.get("copy", "")
        post.hashtags = data.get("hashtags", "")
        post.status = "sent"
        post.updated_at = timezone.now()
        post.save()

        return Response({"success": True})

    except InstagramPost.DoesNotExist:
        return Response(
            {"error": "Post not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    


MODEL_MAP = {
    "InstagramPost": InstagramPost,
    "InstagramReel": InstagramReel,
    "FacebookImagePost": FacebookImagePost,
}


@api_view(['POST'])
@permission_classes([AllowAny])
def generic_callback(request):

    data = request.data

    model_name = data.get("model")
    object_id = data.get("id")
    status_value = data.get("status")

    model = MODEL_MAP.get(model_name)

    if not model:
        return Response(
            {"error": "Invalid model"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        obj = model.objects.get(id=object_id)

        obj.status = status_value
        obj.updated_at = timezone.now()
        obj.save()

        return Response({"success": True})

    except model.DoesNotExist:
        return Response(
            {"error": "Not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )