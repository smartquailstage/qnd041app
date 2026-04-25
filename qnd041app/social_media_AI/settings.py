from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable
from wagtail.images import get_image_model

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
        null=True, blank=True
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

    brand_1 = models.TextField(verbose_name="Brand Principal",
        help_text = "Escriba el brand principal de la campaña", null=True, blank=True)

    brand_2 = models.TextField(verbose_name="Brand Secundario",
        help_text = "Escriba el brand secundario de la campaña", null=True, blank=True)

    logo_1 = models.ForeignKey(
        Image,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text = "Elija la marca principal"
    )

    logo_2 = models.ForeignKey(
        Image,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text = "Elija la marca secundaria"
    )

    color_1 = models.CharField(
        max_length=50,
        verbose_name="Paleta de color primaria",
        help_text="Escriba el codigo RGB o HEX de color primario",
        null=True, blank=True
    )

    color_2 = models.CharField(
        max_length=50,
        verbose_name="Paleta de color secundaria",
        help_text="Escriba el codigo RGB o HEX de color primario",
        null=True, blank=True
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
        help_text="Elija la  tonalidad de la campaña",
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

    def __str__(self):
        return self.name