from django.db import models
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

User = get_user_model()
Image = get_image_model()


# =========================
# 🔹 BASE
# =========================
class BasePost(models.Model):

    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_posts",
        related_query_name="%(app_label)s_%(class)s"
    )

    STATUS_CHOICES = [
        ("draft", "Borrador"),
        ("scheduled", "Programado"),
        ("processing", "Procesando"),
        ("sent", "Enviado"),
        ("failed", "Fallido"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    scheduled_date = models.DateTimeField(null=True, blank=True,help_text = "Asigne una fecha y hora para publicacion automatica",verbose_name="Fecha/Hora")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.core.files.base import ContentFile
from wagtail.images import get_image_model

import requests
from io import BytesIO
from PIL import Image as PILImage


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

        # =========================
        # 1️⃣ Descargar imagen base
        # =========================
        try:
            r = requests.get(image_url, timeout=15)
            r.raise_for_status()
        except Exception as e:
            return Response(
                {"success": False, "message": f"Error descargando imagen: {str(e)}"},
                status=400
            )

        try:
            base_image = PILImage.open(BytesIO(r.content)).convert("RGBA")
        except Exception as e:
            return Response(
                {"success": False, "message": f"Error procesando imagen: {str(e)}"},
                status=400
            )

        # =========================
        # 2️⃣ Insertar logo (SAFE)
        # =========================
        try:
            logo_field = getattr(post.categories, "logo_1", None)

            if logo_field and hasattr(logo_field, "file") and logo_field.file:
                logo_url = logo_field.file.url

                logo_response = requests.get(logo_url, timeout=10)

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

        except Exception as e:
            # No romper el flujo si falla el logo
            print("Error procesando logo:", str(e))

        # =========================
        # 3️⃣ Guardar en Wagtail
        # =========================
        buffer = BytesIO()
        base_image.save(buffer, format="PNG")
        buffer.seek(0)

        ImageModel = get_image_model()

        wagtail_image = ImageModel(
            title=f"Post {post.id} final image",
            file=ContentFile(buffer.read(), name=f"post_{post.id}.png")
        )
        wagtail_image.save()

        # =========================
        # 4️⃣ Guardar URL en modelo
        # =========================
        post.image = wagtail_image.file.url  # ✅ CORRECTO para URLField

        # Opcionales desde n8n
        post.caption = data.get("caption", post.caption)
        post.copy = data.get("copy", post.copy)
        post.hashtags = data.get("hashtags", post.hashtags)

        post.status = data.get("status", "Procesado")

        post.save()

        return Response({
            "success": True,
            "message": "Imagen procesada correctamente",
            "image_url": post.image
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
# =========================
# 🔹 INSTAGRAM CAROUSEL
# =========================
class InstagramCarouselPost(ClusterableModel, BasePost):

    image_size = models.CharField(max_length=20)

    category = models.ForeignKey(
        CategoryItem,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    caption = models.TextField()
    copy = models.TextField(blank=True)
    hashtags = models.TextField()

    panels = [
        FieldPanel("image_size"),
        FieldPanel("category"),
        FieldPanel("caption"),
        FieldPanel("copy"),
        FieldPanel("hashtags"),
        InlinePanel("images", label="Imágenes (máx 10)"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def clean(self):
        if self.pk and self.images.count() > 10:
            raise ValidationError("Máximo 10 imágenes")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.caption[:40]


class InstagramCarouselImage(Orderable):

    post = ParentalKey(
        InstagramCarouselPost,
        related_name="images",
        on_delete=models.CASCADE
    )

    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="+")
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]


# =========================
# 🔹 INSTAGRAM REEL
# =========================
class InstagramReel(BasePost):

    title = models.CharField(max_length=255)

    video = models.ForeignKey(
        Media,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    caption = models.TextField()
    hashtags = models.TextField(blank=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("video"),
        FieldPanel("caption"),
        FieldPanel("hashtags"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


# =========================
# 🔹 FACEBOOK IMAGE
# =========================
class FacebookImagePost(BasePost):

    message = models.TextField()

    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    link = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel("message"),
        FieldPanel("image"),
        FieldPanel("link"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def __str__(self):
        return self.message[:40]

    class Meta:
        ordering = ["-created_at"]


# =========================
# 🔹 FACEBOOK VIDEO
# =========================
class FacebookVideoPost(BasePost):

    message = models.TextField()

    video = models.ForeignKey(
        Media,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    link = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel("message"),
        FieldPanel("video"),
        FieldPanel("link"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def __str__(self):
        return self.message[:40]

    class Meta:
        ordering = ["-created_at"]


# =========================
# 🔹 FACEBOOK CAROUSEL
# =========================
class FacebookCarouselPost(ClusterableModel, BasePost):

    message = models.TextField()
    link = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel("message"),
        FieldPanel("link"),
        InlinePanel("images", label="Imágenes"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def __str__(self):
        return self.message[:40]

    class Meta:
        ordering = ["-created_at"]


class FacebookCarouselImage(Orderable):

    post = ParentalKey(
        FacebookCarouselPost,
        related_name="images",
        on_delete=models.CASCADE
    )

    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="+")
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]


# =========================
# 🔹 TWITTER
# =========================
class TwitterPost(BasePost):

    text = models.CharField(max_length=280)

    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        FieldPanel("text"),
        FieldPanel("image"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def __str__(self):
        return self.text[:40]

    class Meta:
        ordering = ["-created_at"]


# =========================
# 🔹 LINKEDIN
# =========================
class LinkedInPost(BasePost):

    content = models.TextField()

    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    link = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel("content"),
        FieldPanel("image"),
        FieldPanel("link"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def __str__(self):
        return self.content[:50]

    class Meta:
        ordering = ["-created_at"]