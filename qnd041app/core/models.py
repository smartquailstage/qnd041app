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
    Snippet para crear imágenes de marca con Gemini usando opciones predefinidas
    y soporte de logo de la empresa.
    """

    # Opciones para el título del post
    TITLE_CHOICES = [
        ("launch", "Lanzamiento de producto"),
        ("promotion", "Promoción / Oferta"),
        ("event", "Evento especial"),
        ("testimonial", "Testimonio / Historia de cliente"),
        ("educational", "Educativo / Tips"),
        ("fun", "Contenido divertido / meme"),
    ]
    title = models.CharField(
        max_length=255,
        choices=TITLE_CHOICES,
        help_text="Tipo de post para Instagram",
        null=True,
        blank=True
    )

    # Tono de la marca
    BRAND_VOICE_CHOICES = [
        ("friendly", "Amigable"),
        ("professional", "Profesional"),
        ("aspirational", "Aspiracional"),
        ("fun", "Divertido"),
        ("luxury", "Lujoso / Premium"),
        ("techy", "Tecnológico / Innovador"),
    ]
    brand_voice = models.CharField(
        max_length=50,
        choices=BRAND_VOICE_CHOICES,
        blank=True,
        help_text="Tono de la marca"
    )

    # Estilo visual
    STYLE_CHOICES = [
        ("minimal", "Minimalista"),
        ("modern", "Moderno"),
        ("retro", "Retro / Vintage"),
        ("illustrative", "Ilustrativo / Vectorial"),
        ("photorealistic", "Fotorealista"),
        ("cinematic", "Cinemático / Dramático"),
    ]
    style = models.CharField(
        max_length=50,
        choices=STYLE_CHOICES,
        blank=True,
        help_text="Estilo visual de la imagen"
    )

    # Paleta de colores (categorías generales)
    COLOR_PALETTE_CHOICES = [
        ("pastel", "Tonos pastel"),
        ("vibrant", "Colores vibrantes"),
        ("monochrome", "Monocromo"),
        ("dark_mode", "Tonos oscuros"),
        ("light_mode", "Tonos claros"),
    ]
    color_palette = models.CharField(
        max_length=50,
        choices=COLOR_PALETTE_CHOICES,
        blank=True,
        help_text="Categoría de paleta de colores de la imagen"
    )

    # Tipografía
    FONT_STYLE_CHOICES = [
        ("sans_serif", "Sans-serif moderna"),
        ("serif", "Serif clásica"),
        ("handwritten", "Estilo manuscrito"),
        ("display", "Tipografía llamativa / Display"),
    ]
    font_style = models.CharField(
        max_length=50,
        choices=FONT_STYLE_CHOICES,
        blank=True,
        help_text="Tipo de tipografía para el texto de la imagen"
    )

    # Formato de imagen
    FORMAT_CHOICES = [
        ("square", "Cuadrado 1080x1080px"),
        ("portrait", "Vertical 1080x1350px"),
        ("landscape", "Horizontal 1080x566px"),
        ("story", "Historia de Instagram 1080x1920px"),
    ]
    format = models.CharField(
        max_length=50,
        choices=FORMAT_CHOICES,
        blank=True,
        help_text="Formato de imagen para publicación"
    )

    # Textos para la imagen
    title_text = models.TextField(
        blank=True,
        help_text="Texto principal / título que aparecerá en la imagen"
    )
    brand_text = models.TextField(
        blank=True,
        help_text="Texto de la marca que aparecerá en la imagen (slogan o mensaje)"
    )
    company_info_text = models.TextField(
        blank=True,
        help_text="Información adicional de la empresa para la imagen (website, contacto, descriptor)"
    )

    # Logo de la empresa
    company_logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True,
        help_text="Logo de la empresa para incluir en la imagen"
    )

    # Estado del post
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("processing", "Procesando"),
        ("completed", "Completado"),
        ("error", "Error"),
    ]
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Estado del post"
    )

    scheduled_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha programada para el posteo (opcional)"
    )

        # URL de la imagen generada por n8n / Gemini
    generated_image_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL de la imagen generada por la IA y almacenada en el bucket"
    )


    panels = [
        FieldPanel("title"),
        FieldPanel("brand_voice"),
        FieldPanel("style"),
        FieldPanel("color_palette"),
        FieldPanel("font_style"),
        FieldPanel("format"),
        FieldPanel("title_text"),
        FieldPanel("brand_text"),
        FieldPanel("company_info_text"),
        FieldPanel("company_logo"),
        FieldPanel("scheduled_datetime"),
        FieldPanel("status"),
        FieldPanel("generated_image_url"),  # Panel para la URL generada
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