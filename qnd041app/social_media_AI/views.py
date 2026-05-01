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
            text = "All copyrights ® reserved 2026 SmartQuail, Inc"
            
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
def update_generated_carousel_slide(request):
    try:
        data = request.data
        post_id = data.get("originalId") or data.get("original_id")
        slide_index = int(data.get("slide_index", 1))
        image_url = data.get("image_url")

        if not post_id or not image_url:
            return Response({"success": False, "message": "Datos incompletos"}, status=400)

        post = InstagramCarouselPost.objects.get(id=post_id)
        cat = post.categories
        ImageModel = get_image_model()

        # =========================
        # 1️⃣ Descargar imagen base
        # =========================
        r = requests.get(image_url, timeout=20)
        r.raise_for_status()
        base_image = PILImage.open(BytesIO(r.content)).convert("RGBA")
        base_width, base_height = base_image.size
        margin = 40

        # =========================
        # 2️⃣ Branding Dinámico
        # =========================
        # Slide 1: Logos en esquinas
        if slide_index == 1:
            # Logo 1 - Top Left
            if cat and cat.logo_1:
                res = requests.get(cat.logo_1.file.url)
                logo = PILImage.open(BytesIO(res.content)).convert("RGBA")
                logo.thumbnail((base_width * 0.20, base_height * 0.20), PILImage.LANCZOS)
                base_image.paste(logo, (margin, margin), logo)
            
            # Logo 2 - Bottom Right
            if cat and cat.logo_2:
                res = requests.get(cat.logo_2.file.url)
                logo = PILImage.open(BytesIO(res.content)).convert("RGBA")
                logo.thumbnail((base_width * 0.15, base_height * 0.15), PILImage.LANCZOS)
                base_image.paste(logo, (base_width - logo.size[0] - margin, base_height - logo.size[1] - margin), logo)

        # Último Slide: Logo centrado y legales
        elif slide_index == post.slides:
            if cat and cat.logo_1:
                res = requests.get(cat.logo_1.file.url)
                logo = PILImage.open(BytesIO(res.content)).convert("RGBA")
                logo.thumbnail((base_width * 0.35, base_height * 0.35), PILImage.LANCZOS)
                x = (base_width - logo.size[0]) // 2
                y = (base_height - logo.size[1]) // 2
                base_image.paste(logo, (x, y), logo)

            text = "All copyrights ® reserved 2026 SmartQuail, Inc"
            draw = ImageDraw.Draw(base_image)
            
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
            

        # =========================
        # 3️⃣ Guardar en Wagtail e Inline
        # =========================
        buffer = BytesIO()
        base_image.save(buffer, format="PNG")
        buffer.seek(0) # 👈 IMPORTANTE: Volver al inicio del buffer antes de guardar
        
        ImageModel = get_image_model()
        wagtail_image = ImageModel(title=f"Post {post.id} - Slide {slide_index}")
        wagtail_image.file.save(f"carousel_{post.id}_{slide_index}.png", ContentFile(buffer.getvalue()), save=True)

        # Buscamos si el slide ya existe o lo creamos
        # Usamos update_or_create para manejar los re-intentos de n8n
        from .models import InstagramCarouselImage
        slide, created = InstagramCarouselImage.objects.update_or_create(
            post=post,
            sort_order=slide_index - 1, # Wagtail usa sort_order para el orden
            defaults={
                'image': wagtail_image,
                'caption': data.get("caption", ""),
                'copy': data.get("copy", ""),
                'hashtags': data.get("hashtags", ""),
            }
        )

        # =========================
        # 4️⃣ Verificar si el carrusel está completo
        # =========================
        if post.images.count() >= post.slides:
            post.status = "sent"
            post.save(update_fields=["status"])

        return Response({"success": True, "slide": slide_index})

    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=500)



@api_view(['POST'])
@permission_classes([AllowAny])
def update_generated_reel(request):
    """
    Recibe el video final de n8n y actualiza el modelo InstagramReel.
    """
    try:
        data = request.data
        # n8n envía 'originalId'
        reel_id = data.get("originalId") or data.get("original_id")
        video_url = data.get("video_url") or data.get("generated_video_url")

        if not reel_id or not video_url:
            return Response({"success": False, "message": "ID de Reel o URL de video ausentes"}, status=400)

        # Importación local para evitar problemas de carga
        from .models import InstagramReel
        reel = InstagramReel.objects.get(id=reel_id)

        # 1️⃣ Actualizar Metadatos (Textos)
        # Guardamos lo que generó la IA
        reel.caption = data.get("caption") or reel.caption or ""
        reel.copy = data.get("copy") or reel.copy or ""
        reel.hashtags = data.get("hashtags") or reel.hashtags or ""
        reel.generated_video_url = video_url # Guardamos la URL externa como respaldo

        # 2️⃣ Descargar y Guardar el archivo de Video
        try:
            print(f"📥 Descargando video para Reel {reel.id}...")
            # Aumentamos el timeout porque los archivos de video son pesados
            response = requests.get(video_url, timeout=120)
            response.raise_for_status()

            # Creamos un nombre de archivo único
            timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
            file_name = f"reel_final_{reel.id}_{timestamp}.mp4"

            # Guardamos en el FileField del modelo
            reel.video.save(
                file_name, 
                ContentFile(response.content), 
                save=False # Todavía no guardamos el modelo completo
            )
        except Exception as e:
            print(f"⚠️ Error al descargar el archivo físico: {e}")
            # No bloqueamos el proceso, ya tenemos la URL externa de respaldo

        # 3️⃣ Finalizar Estado
        reel.status = "sent"
        reel.updated_at = timezone.now()
        
        # Guardamos todos los cambios
        reel.save()

        return Response({
            "success": True, 
            "message": f"Reel {reel.id} actualizado correctamente",
            "local_file": reel.video.url if reel.video else None
        })

    except InstagramReel.DoesNotExist:
        return Response({"success": False, "message": "Reel no encontrado"}, status=404)
    except Exception as e:
        print(f"💥 Error en update_generated_reel: {str(e)}")
        return Response({"success": False, "message": str(e)}, status=500)



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