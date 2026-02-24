from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class SocialAutomationPost(models.Model):
    """
    Snippet que almacena prompts de SocialAutomation
    para generar contenido con Gemini y Canva.
    """

    prompt = models.TextField(help_text="Prompt para generar el contenido con Gemini")
    brand_voice = models.CharField(max_length=255, blank=True)
    scheduled_datetime = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default="pending")

    panels = [
        FieldPanel("prompt"),
        FieldPanel("brand_voice"),
        FieldPanel("scheduled_datetime"),
        FieldPanel("status"),
    ]

    class Meta:
        verbose_name = "Social Automation Post"
        verbose_name_plural = "Social Automation Posts"
        ordering = ["-scheduled_datetime"]

    def __str__(self):
        return f"Post #{self.id}"



# core/models.py

# core/models.py

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.images import get_image_model_string


@register_snippet
class GeneratedSocialAsset(models.Model):

    social_post = models.ForeignKey(
        "core.SocialAutomationPost",
        on_delete=models.CASCADE,
        related_name="generated_assets"
    )

    caption = models.TextField(blank=True)

    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    meta_post_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default="generated")

    panels = [
        FieldPanel("social_post"),
        FieldPanel("caption"),
        FieldPanel("image"),
        FieldPanel("meta_post_id"),
        FieldPanel("status"),
    ]

    class Meta:
        verbose_name = "Generated Social Asset"
        verbose_name_plural = "Generated Social Assets"
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