from django.db import models
from django.core.validators import RegexValidator

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.fields import RichTextField
from wagtail.models import Orderable


ecuador_phone_validator = RegexValidator(
    regex=r'^\+593\d{8,9}$',
    message="El número debe tener formato Ecuador: +593XXXXXXXXX"
)

class Conversation(ClusterableModel):
    INTERACTION_CHOICES = [
        ("venta", "Venta"),
        ("info", "Solicitud de información"),
    ]

    SENTIMENT_CHOICES = [
        ("positivo", "Positivo"),
        ("neutral", "Neutral"),
        ("negativo", "Negativo"),
    ]

    username = models.CharField(max_length=255)
    phone = models.CharField(
        max_length=13,
        validators=[ecuador_phone_validator]
    )

    interaction_type = models.CharField(
        max_length=20,
        choices=INTERACTION_CHOICES
    )

    sentiment = models.CharField(
        max_length=20,
        choices=SENTIMENT_CHOICES,
        default="neutral"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel("username"),
        FieldPanel("phone"),
        FieldPanel("interaction_type"),
        FieldPanel("sentiment"),
        InlinePanel("messages", label="Chat"),
    ]

    def __str__(self):
        return f"{self.username} - {self.phone}"


class Message(Orderable):
    conversation = ParentalKey(
        Conversation,
        related_name="messages",
        on_delete=models.CASCADE
    )

    ROLE_CHOICES = [
        ("user", "Usuario"),
        ("bot", "Bot"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel("role"),
        FieldPanel("content"),
    ]

    def __str__(self):
        return f"{self.role}: {self.content[:30]}"