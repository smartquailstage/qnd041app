from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from django.db import models

from django.utils.functional import cached_property

# core/models.py

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.images import get_image_model_string

# ----------------------------------------
# 1️⃣ Snippet: crea la imagen con Gemini
# ----------------------------------------
@register_snippet
class SocialAutomationPost(models.Model):
    """
    Snippet para crear imágenes de marca con Gemini
    """

    title = models.CharField(
        max_length=255,
        help_text="Título del post",
        null=True,
        blank=True
    )
    prompt = models.TextField(
        help_text="Prompt para generar el contenido con Gemini"
    )
    brand_voice = models.CharField(
        max_length=255,
        blank=True,
        help_text="Tono de la marca"
    )
    brand_text = models.TextField(
        blank=True,
        help_text="Texto de la marca para incluir en la imagen"
    )
    scheduled_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha programada para el posteo (opcional)"
    )
    status = models.CharField(
        max_length=50,
        default="pending",
        help_text="Estado del post: pending, processing, completed, error"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("prompt"),
        FieldPanel("brand_voice"),
        FieldPanel("brand_text"),
        FieldPanel("scheduled_datetime"),
        FieldPanel("status"),
    ]

    class Meta:
        verbose_name = "AI Content Image Creator"
        verbose_name_plural = "AI Content Image Creators"
        ordering = ["-scheduled_datetime"]

    def __str__(self):
        return f"{self.title or f'Brand Post #{self.id}'}"


# ----------------------------------------
# 2️⃣ Snippet: guarda la imagen final editada
# ----------------------------------------
@register_snippet
class GeneratedSocialAsset(models.Model):
    """
    Snippet que almacena la imagen final generada para redes sociales
    """

    social_post = models.ForeignKey(
        "core.SocialAutomationPost",
        on_delete=models.CASCADE,
        related_name="generated_assets"
    )

    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Imagen final editada"
    )

    reference_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Imagen de referencia desde SocialAutomationPost"
    )

    logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Logo de la marca a incluir"
    )

    caption = models.TextField(
        blank=True,
        help_text="Texto o caption para redes sociales"
    )

    meta_post_id = models.CharField(
        max_length=255,
        blank=True,
        help_text="ID del post en Meta (Instagram/Facebook)"
    )

    status = models.CharField(
        max_length=50,
        default="generated",
        help_text="Estado del asset: generated, sent_to_n8n, error"
    )

    panels = [
        FieldPanel("social_post"),
        FieldPanel("caption"),
        FieldPanel("image"),
        FieldPanel("reference_image"),
        FieldPanel("logo"),
        FieldPanel("meta_post_id"),
        FieldPanel("status"),
    ]

    class Meta:
        verbose_name = "AI Brand Image Generation"
        verbose_name_plural = "AI Brand Image Generations"
        ordering = ["-id"]

    def __str__(self):
        return f"Asset for Post #{self.social_post.id}"



from django.db import models
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from wagtail.snippets.models import register_snippet
from django.utils import timezone


@register_snippet
class SocialPostSchedule(models.Model):
    """
    Snippet para programar publicaciones en Meta usando
    imágenes generadas previamente.
    """

    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("scheduled", "Programado"),
        ("posted", "Publicado"),
        ("error", "Error"),
    ]

    PLATFORM_CHOICES = [
        ("instagram", "Instagram"),
        ("facebook", "Facebook"),
        ("both", "Ambos"),
    ]

    image = models.ForeignKey(
        GeneratedSocialAsset,
        on_delete=models.CASCADE,
        related_name="scheduled_posts",
        help_text="Selecciona la imagen generada previamente"
    )
    scheduled_datetime = models.DateTimeField(default=timezone.now)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, default="both")
    caption = models.TextField(blank=True)
    meta_post_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    panels = [
        FieldPanel("image"),
        FieldPanel("scheduled_datetime"),
        FieldPanel("platform"),
        FieldPanel("caption"),
        FieldPanel("status"),
    ]

    def __str__(self):
        return f"Scheduled Post #{self.id} - {self.status}"