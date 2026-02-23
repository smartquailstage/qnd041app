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