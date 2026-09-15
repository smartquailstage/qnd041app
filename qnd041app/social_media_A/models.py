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
        related_name="%(class)s_posts"
    )

    STATUS_CHOICES = [
        ("draft", "Borrador"),
        ("scheduled", "Programado"),
        ("processing", "Procesando"),
        ("sent", "Enviado"),
        ("failed", "Fallido"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    scheduled_date = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        abstract = True


from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


#@register_snippet
class InstagramAccount(models.Model):
    """
    Modelo Snippet para gestionar cuentas de Instagram desde Wagtail.
    """
    account_name = models.CharField(
        max_length=100,
        verbose_name="Nombre de la cuenta",
        help_text="Ejemplo: @mi_empresa o Nombre Visible"
    )
    account_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="ID de Instagram",
        help_text="ID numérico o identificador único de la cuenta/API de Instagram"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="¿Activa?",
        help_text="Indica si esta cuenta está disponible para su uso en el sitio"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    # Configuración de los campos visibles en el formulario de Wagtail
    panels = [
        FieldPanel('account_name'),
        FieldPanel('account_id'),
        FieldPanel('is_active'),
    ]

    # Columnas visibles en la lista del panel de administración de Wagtail
    admin_cols = ['account_name', 'account_id', 'is_active', 'created_at']

    class Meta:
        verbose_name = "Cuenta de Instagram"
        verbose_name_plural = "Cuentas de Instagram"
        ordering = ['account_name']

    def __str__(self):
        return f"{self.account_name} ({self.account_id})"

# =========================
# 🔹 INSTAGRAM POST
# =========================
class InstagramPost(BasePost):

    account = models.ForeignKey(
        InstagramAccount,
        null=True,
        blank=True, 
        on_delete=models.SET_NULL
    )

    IMAGE_SIZE_CHOICES = [
        ('square', 'Cuadrado'),
        ('vertical', 'Vertical'),
        ('horizontal', 'Horizontal'),
        ('story', 'Story'),
    ]

    image_size = models.CharField(max_length=20, choices=IMAGE_SIZE_CHOICES)

    categories = models.ForeignKey(
        CategoryItem,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    caption = models.TextField()
    copy = models.TextField(blank=True)
    hashtags = models.TextField()

    image = models.ForeignKey(
        Image,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        FieldPanel("account"),
        FieldPanel("image_size"),
        FieldPanel("categories"),
        FieldPanel("caption"),
        FieldPanel("copy"),
        FieldPanel("hashtags"),
        FieldPanel("image"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def image_thumb(self):
        if self.image:
            return format_html(
                '<img src="{}" style="width:60px;height:60px;object-fit:cover;" />',
                self.image.get_rendition("fill-120x120").url
            )
        return "—"

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.caption[:40]


# =========================
# 🔹 INSTAGRAM CAROUSEL
# =========================
class InstagramCarouselPost(BasePost, ClusterableModel):

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
        InlinePanel("images", label="Imágenes"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def clean(self):
        if self.images.count() > 10:
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
class FacebookCarouselPost(BasePost, ClusterableModel):

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