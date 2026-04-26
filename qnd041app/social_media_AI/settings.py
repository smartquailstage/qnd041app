from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable
from wagtail.images import get_image_model
from django.conf import settings

Image = get_image_model()

@register_setting
class SocialMediaSettings(BaseGenericSetting, ClusterableModel):
    panels = [
        InlinePanel('categories', label="Campañas")
    ]


class CategoryItem(Orderable):
    settings = ParentalKey(
        SocialMediaSettings,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=50,
        verbose_name="Nombre",
        help_text="Define el nombre principal de la campaña."
    )

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
        help_text="Elija el estilo visual de la campaña"
    )

    brand_1 = models.TextField(
        verbose_name="Brand Principal",
        help_text="Escriba el brand principal de la campaña",
        null=True,
        blank=True
    )

    brand_2 = models.TextField(
        verbose_name="Brand Secundario",
        help_text="Escriba el brand secundario de la campaña",
        null=True,
        blank=True
    )

    logo_1 = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Elija la marca principal"
    )

    logo_2 = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Elija la marca secundaria"
    )

    # =========================
    # 🔥 URLs AUTOMÁTICAS
    # =========================
    image_url_1 = models.URLField(max_length=500,blank=True, null=True, editable=False)
    image_url_2 = models.URLField(max_length=500,blank=True, null=True, editable=False)

    color_1 = models.CharField(
        max_length=50,
        verbose_name="Paleta de color primaria",
        null=True,
        blank=True
    )

    color_2 = models.CharField(
        max_length=50,
        verbose_name="Paleta de color secundaria",
        null=True,
        blank=True
    )

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
        null=True
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('style'),
        FieldPanel('brand_1'),
        FieldPanel('brand_2'),
        FieldPanel('logo_1'),
        FieldPanel('logo_2'),
        FieldPanel('color_1'),
        FieldPanel('color_2'),
        FieldPanel('color_palette'),
    ]

    # =========================
    # 🔥 CORE: URL BUILDER
    # =========================
    def _build_absolute_url(self, image):
        """
        Devuelve una URL válida:
        - S3/CDN → la deja igual
        - local → la convierte en absoluta
        """
        if not image:
            return None

        try:
            url = image.file.url
        except Exception:
            return None

        # Ya es absoluta (S3, CDN)
        if url.startswith("http://") or url.startswith("https://"):
            return url

        # Construir absoluta en local
        base = getattr(settings, "BASE_URL", "")
        return f"{base}{url}" if base else url

    # =========================
    # 🔥 SET URLS
    # =========================
    def set_image_urls(self):
        self.image_url_1 = self._build_absolute_url(self.logo_1)
        self.image_url_2 = self._build_absolute_url(self.logo_2)

    # =========================
    # 🔥 SAVE HOOK
    # =========================
    def save(self, *args, **kwargs):
        self.set_image_urls()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name