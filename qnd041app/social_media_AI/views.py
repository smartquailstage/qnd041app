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



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.core.files.base import ContentFile
from wagtail.images import get_image_model

import requests
from io import BytesIO
from PIL import Image as PILImage, ImageDraw, ImageFont


import requests
from io import BytesIO
from PIL import Image as PILImage, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from wagtail.images import get_image_model
from .models import InstagramPost

@api_view(['POST'])
@permission_classes([AllowAny])
def update_generated_image(request):
    try:
        data = request.data
        post_id = data.get("id")
        image_url = data.get("image")

        if not post_id or not image_url:
            return Response({"success": False, "message": "id o image faltantes"}, status=400)

        # Buscamos el post por ID
        post = InstagramPost.objects.get(id=post_id)

        # =========================
        # 1️⃣ Descargar imagen base
        # =========================
        try:
            r = requests.get(image_url, timeout=15)
            r.raise_for_status()
            base_image = PILImage.open(BytesIO(r.content)).convert("RGBA")
        except Exception as e:
            return Response({"success": False, "message": f"Error descargando imagen: {str(e)}"}, status=400)

        # =========================
        # 2️⃣ Insertar Branding (Logos y Copyright)
        # =========================
        try:
            base_width, base_height = base_image.size
            margin = 40 
            
            # --- LOGO 1: Esquina Superior Izquierda ---
            # Corregido: Usamos 'post.categories'
            logo1_field = getattr(post.categories, "logo_1", None)
            if logo1_field and hasattr(logo1_field, "file") and logo1_field.file:
                logo1_res = requests.get(logo1_field.file.url, timeout=10)
                if logo1_res.status_code == 200:
                    logo1 = PILImage.open(BytesIO(logo1_res.content)).convert("RGBA")
                    max_w = int(base_width * 0.20)
                    ratio = max_w / logo1.size[0]
                    logo1 = logo1.resize((max_w, int(logo1.size[1] * ratio)), PILImage.LANCZOS)
                    # Pegar en (40, 40)
                    base_image.paste(logo1, (margin, margin), logo1)

            # --- LOGO 2: Esquina Inferior Derecha ---
            logo2_field = getattr(post.categories, "logo_2", None)
            if logo2_field and hasattr(logo2_field, "file") and logo2_field.file:
                logo2_res = requests.get(logo2_field.file.url, timeout=10)
                if logo2_res.status_code == 200:
                    logo2 = PILImage.open(BytesIO(logo2_res.content)).convert("RGBA")
                    max_w = int(base_width * 0.15)
                    ratio = max_w / logo2.size[0]
                    logo2 = logo2.resize((max_w, int(logo2.size[1] * ratio)), PILImage.LANCZOS)
                    
                    x_l2 = base_width - logo2.size[0] - margin
                    y_l2 = base_height - logo2.size[1] - margin
                    base_image.paste(logo2, (x_l2, y_l2), logo2)

            # --- COPYRIGHT: Centro Inferior ---
            draw = ImageDraw.Draw(base_image)
            text = "All copyrights reserved 2026"
            
            try:
                # Intenta cargar Arial, si falla usa la default
                font = ImageFont.truetype("arial.ttf", 28)
            except:
                font = ImageFont.load_default()

            if hasattr(draw, 'textbbox'):
                l, t, r, b = draw.textbbox((0, 0), text, font=font)
                tw = r - l
            else:
                tw, _ = draw.textsize(text, font=font)

            x_text = (base_width - tw) // 2
            y_text = base_height - margin - 20

            # Sombra para legibilidad y texto blanco
            draw.text((x_text + 1, y_text + 1), text, fill="black", font=font)
            draw.text((x_text, y_text), text, fill="white", font=font)
            
        except Exception as e:
            print(f"⚠️ Error en el branding: {e}")

        # =========================
        # 3️⃣ Guardar en Wagtail
        # =========================
        buffer = BytesIO()
        # Guardamos como PNG para mantener transparencias de logos si las hay
        base_image.save(buffer, format="PNG")
        image_file = ContentFile(buffer.getvalue())

        ImageModel = get_image_model()
        wagtail_image = ImageModel(title=f"Post {post.id} Final")
        # El método save() del campo file se encarga de subirlo al storage (S3/Local)
        wagtail_image.file.save(f"post_{post.id}.png", image_file, save=True)

        # =========================
        # 4️⃣ Actualizar el modelo
        # =========================
        post.image = wagtail_image.file.url
        post.caption = data.get("caption", post.caption)
        post.copy = data.get("copy", post.copy)
        post.hashtags = data.get("hashtags", post.hashtags)
        post.status = "sent" # O el estado que envíe n8n
        post.save()

        return Response({
            "success": True,
            "message": "Imagen procesada con branding y guardada",
            "image_url": post.image
        })

    except InstagramPost.DoesNotExist:
        return Response({"success": False, "message": "Post no encontrado"}, status=404)
    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=500)




@api_view(['POST'])
@permission_classes([AllowAny])
def update_generated_carousel(request):
    try:
        data = request.data
        post_id = data.get("post_id")
        images_data = data.get("images", [])

        if not post_id or not images_data:
            return Response(
                {"success": False, "message": "post_id o images faltantes"},
                status=400
            )

        post = InstagramCarouselPost.objects.get(id=post_id)
        cat = post.categories

        ImageModel = get_image_model()

        for index, img_data in enumerate(images_data):
            item_id = img_data.get("id")
            image_url = img_data.get("image")

            if not item_id or not image_url:
                continue

            try:
                item = post.images.get(id=item_id)
            except:
                continue

            # =========================
            # 1️⃣ Descargar imagen
            # =========================
            try:
                r = requests.get(image_url, timeout=15)
                r.raise_for_status()
                base_image = PILImage.open(BytesIO(r.content)).convert("RGBA")
            except Exception as e:
                print(f"❌ Error descargando imagen {item_id}: {e}")
                continue

            base_width, base_height = base_image.size
            margin = 40

            # =========================
            # 2️⃣ BRANDING SEGÚN POSICIÓN
            # =========================
            try:
                # -------- PRIMERA IMAGEN --------
                if index == 0:
                    # Logo 1 (top-left)
                    logo1_field = getattr(cat, "logo_1", None)
                    if logo1_field and hasattr(logo1_field, "file"):
                        res = requests.get(logo1_field.file.url, timeout=10)
                        if res.status_code == 200:
                            logo1 = PILImage.open(BytesIO(res.content)).convert("RGBA")
                            max_w = int(base_width * 0.20)
                            ratio = max_w / logo1.size[0]
                            logo1 = logo1.resize((max_w, int(logo1.size[1] * ratio)), PILImage.LANCZOS)
                            base_image.paste(logo1, (margin, margin), logo1)

                    # Logo 2 (bottom-right)
                    logo2_field = getattr(cat, "logo_2", None)
                    if logo2_field and hasattr(logo2_field, "file"):
                        res = requests.get(logo2_field.file.url, timeout=10)
                        if res.status_code == 200:
                            logo2 = PILImage.open(BytesIO(res.content)).convert("RGBA")
                            max_w = int(base_width * 0.15)
                            ratio = max_w / logo2.size[0]
                            logo2 = logo2.resize((max_w, int(logo2.size[1] * ratio)), PILImage.LANCZOS)

                            x = base_width - logo2.size[0] - margin
                            y = base_height - logo2.size[1] - margin
                            base_image.paste(logo2, (x, y), logo2)

                # -------- ÚLTIMA IMAGEN --------
                if index == len(images_data) - 1:
                    draw = ImageDraw.Draw(base_image)

                    # Logo 1 centrado
                    logo1_field = getattr(cat, "logo_1", None)
                    if logo1_field and hasattr(logo1_field, "file"):
                        res = requests.get(logo1_field.file.url, timeout=10)
                        if res.status_code == 200:
                            logo = PILImage.open(BytesIO(res.content)).convert("RGBA")
                            max_w = int(base_width * 0.30)
                            ratio = max_w / logo.size[0]
                            logo = logo.resize((max_w, int(logo.size[1] * ratio)), PILImage.LANCZOS)

                            x = (base_width - logo.size[0]) // 2
                            y = (base_height - logo.size[1]) // 2
                            base_image.paste(logo, (x, y), logo)

                    # Texto inferior
                    try:
                        font = ImageFont.truetype("arial.ttf", 28)
                    except:
                        font = ImageFont.load_default()

                    text_main = "All copyrights reserved 2026"
                    text_url = "https://ec.smartquail.io"

                    def draw_centered_text(text, y_offset):
                        if hasattr(draw, "textbbox"):
                            l, t, r, b = draw.textbbox((0, 0), text, font=font)
                            tw = r - l
                        else:
                            tw, _ = draw.textsize(text, font=font)

                        x = (base_width - tw) // 2
                        y = base_height - margin - y_offset

                        draw.text((x + 1, y + 1), text, fill="black", font=font)
                        draw.text((x, y), text, fill="white", font=font)

                    draw_centered_text(text_main, 50)
                    draw_centered_text(text_url, 10)

            except Exception as e:
                print(f"⚠️ Error branding item {item_id}: {e}")

            # =========================
            # 3️⃣ Guardar imagen
            # =========================
            buffer = BytesIO()
            base_image.save(buffer, format="PNG")
            image_file = ContentFile(buffer.getvalue())

            wagtail_image = ImageModel(title=f"Carousel {post.id} - {item.id}")
            wagtail_image.file.save(f"carousel_{post.id}_{item.id}.png", image_file, save=True)

            # =========================
            # 4️⃣ Actualizar inline
            # =========================
            item.image = wagtail_image
            item.caption = img_data.get("caption", item.caption)
            item.copy = img_data.get("copy", item.copy)
            item.hashtags = img_data.get("hashtags", item.hashtags)

            item.save()

        # =========================
        # 5️⃣ FINALIZAR POST
        # =========================
        post.status = "sent"
        post.save(update_fields=["status"])

        return Response({
            "success": True,
            "message": "Carousel procesado correctamente"
        })

    except InstagramCarouselPost.DoesNotExist:
        return Response({"success": False, "message": "Post no encontrado"}, status=404)

    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=500)

        
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