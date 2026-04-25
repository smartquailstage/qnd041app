from django.db import models
from django.contrib.auth import get_user_model
from wagtail.admin.panels import FieldPanel
from .settings import CategoryItem
from django.utils.html import format_html

from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from wagtailmedia.models import Media  


User = get_user_model()

class InstagramPost(models.Model):

    IMAGE_SIZE_CHOICES = [
        ('square', 'Cuadrado (1:1)'),
        ('vertical', 'Vertical (4:5)'),
        ('horizontal', 'Horizontal (16:9)'),
        ('story', 'Story (9:16)'),
    ]

    image_size = models.CharField(
        max_length=20,
        choices=IMAGE_SIZE_CHOICES,
        verbose_name="Tamaño de imagen",
        help_text="Selecciona el formato del post según el tipo de contenido."
    )

    def image_thumb(self):
        if self.image:
            return format_html(
                '<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:6px;" />',
                self.image.get_rendition("fill-120x120").url
            )
        return "—"

    image_thumb.short_description = "Imagen"

    categories = models.ForeignKey(
        CategoryItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Categoría",
        help_text="Selecciona una única categoría para este post."
    )
    caption = models.TextField(
        verbose_name="Caption",
        help_text="Texto principal del post visible en Instagram."
    )

    copy = models.TextField(
        verbose_name="Copy",
        blank=True,
        help_text="Texto adicional o guía creativa."
    )

    hashtags = models.TextField(
        verbose_name="Hashtags",
        help_text="Separar por espacios o comas. Ej: #marketing #ventas"
    )

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagen",
        help_text="Imagen principal del post."
    )

    scheduled_date = models.DateTimeField(
        verbose_name="Fecha programada",
        help_text="Fecha y hora de publicación."
    )

    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Usuario creador",
        help_text="Usuario responsable del post."
    )

    

    panels = [
        FieldPanel('image_size'),
        FieldPanel('categories'),
        FieldPanel('caption'),
        FieldPanel('copy'),
        FieldPanel('hashtags'),
        FieldPanel('image'),
        FieldPanel('scheduled_date'),
        FieldPanel('created_by'),
    ]


    class Meta:
        verbose_name = "Instagram Post"
        verbose_name_plural = "Instagram Post"

    def __str__(self):
        return self.caption[:40]



from modelcluster.models import ClusterableModel

class InstagramCarouselPost(ClusterableModel, models.Model):

    IMAGE_SIZE_CHOICES = [
        ('square', 'Cuadrado (1:1)'),
        ('vertical', 'Vertical (4:5)'),
        ('horizontal', 'Horizontal (16:9)'),
        ('story', 'Story (9:16)'),
    ]

    image_size = models.CharField(
        max_length=20,
        choices=IMAGE_SIZE_CHOICES,
        verbose_name="Tamaño de imagen",
        help_text="Formato general del carousel."
    )

    category = models.ForeignKey(
        CategoryItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Categoría"
    )

    caption = models.TextField(verbose_name="Caption")

    copy = models.TextField(blank=True, verbose_name="Copy")

    hashtags = models.TextField(verbose_name="Hashtags")

    scheduled_date = models.DateTimeField(verbose_name="Fecha programada")

    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    panels = [
        FieldPanel("image_size"),
        FieldPanel("category"),
        FieldPanel("caption"),
        FieldPanel("copy"),
        FieldPanel("hashtags"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),

        InlinePanel("images", label="Imágenes del Carousel (máx 10)"),
    ]

    def __str__(self):
        return self.caption[:40]

    def clean(self):
        if self.images.count() > 10:
            raise ValidationError("Máximo 10 imágenes permitidas")

    class Meta:
        verbose_name = "Instagram Carousel Post"
        verbose_name_plural = "Instagram Carousels Post"

from modelcluster.models import ClusterableModel

class InstagramCarouselImage(Orderable):

    post = ParentalKey(
        InstagramCarouselPost,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+"
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
        help_text="Texto opcional por imagen"
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]

    def image_thumb(self):
        if self.image:
            return format_html(
                '<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:6px;" />',
                self.image.get_rendition("fill-120x120").url
            )
        return "—"

    image_thumb.short_description = "Preview"



class InstagramReel(ClusterableModel, models.Model):

    title = models.CharField(
        max_length=255,
        verbose_name="Título del Reel",
        help_text="Nombre interno del reel para organización."
    )

    video = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Video del Reel",
        help_text="Selecciona o sube un video (MP4 recomendado)."
    )

    caption = models.TextField(
        verbose_name="Caption",
        help_text="Texto del reel en Instagram."
    )

    hashtags = models.TextField(
        blank=True,
        verbose_name="Hashtags",
        help_text="Ej: #reels #marketing #viral"
    )

    scheduled_date = models.DateTimeField(
        verbose_name="Fecha programada",
        help_text="Fecha de publicación del reel."
    )

    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Usuario creador"
    )

    panels = [
    FieldPanel("title"),
    FieldPanel("video"),  # 👈 aquí aparece el chooser de wagtailmedia
    FieldPanel("caption"),
    FieldPanel("hashtags"),
    FieldPanel("scheduled_date"),
    FieldPanel("created_by"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Instagram Reel"
        verbose_name_plural = "Instagram Reels"



class FacebookImagePost(ClusterableModel, models.Model):

    message = models.TextField(
        verbose_name="Mensaje",
        help_text="Texto principal del post en Facebook."
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Imagen",
        help_text="Imagen principal del post."
    )

    link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Enlace",
        help_text="Opcional: enlace adjunto al post."
    )

    scheduled_date = models.DateTimeField(
        verbose_name="Fecha programada"
    )

    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def image_thumb(self):
        if self.image:
            return format_html(
                '<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:6px;" />',
                self.image.get_rendition("fill-120x120").url
            )
        return "—"

    image_thumb.short_description = "Imagen"

    panels = [
        FieldPanel("message"),
        FieldPanel("image"),
        FieldPanel("link"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def __str__(self):
        return self.message[:40]


from wagtailmedia.models import Media


class FacebookVideoPost(ClusterableModel, models.Model):

    message = models.TextField(
        verbose_name="Mensaje"
    )

    video = models.ForeignKey(
        Media,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Video",
        help_text="Selecciona un video desde Media Library."
    )

    link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Enlace"
    )

    scheduled_date = models.DateTimeField()

    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    panels = [
        FieldPanel("message"),
        FieldPanel("video"),  # 👈 Media chooser
        FieldPanel("link"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def __str__(self):
        return self.message[:40]




from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import InlinePanel


class FacebookCarouselPost(ClusterableModel, models.Model):

    message = models.TextField(
        verbose_name="Mensaje"
    )

    link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Enlace"
    )

    scheduled_date = models.DateTimeField()

    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    panels = [
        FieldPanel("message"),
        FieldPanel("link"),
        InlinePanel("images", label="Imágenes del Carousel"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def __str__(self):
        return self.message[:40]


class FacebookCarouselImage(Orderable):

    post = ParentalKey(
        FacebookCarouselPost,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+"
    )

    caption = models.CharField(
        max_length=255,
        blank=True
    )

    def image_thumb(self):
        if self.image:
            return format_html(
                '<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:6px;" />',
                self.image.get_rendition("fill-120x120").url
            )
        return "—"

    image_thumb.short_description = "Preview"





class TwitterPost(ClusterableModel, models.Model):

    text = models.CharField(
        max_length=280,
        verbose_name="Texto del Tweet",
        help_text="Máximo 280 caracteres."
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Imagen",
        help_text="Opcional: imagen para el tweet."
    )

    scheduled_date = models.DateTimeField(
        verbose_name="Fecha programada"
    )

    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    panels = [
        FieldPanel("text"),
        FieldPanel("image"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def __str__(self):
        return self.text[:40]



class LinkedInPost(ClusterableModel, models.Model):

    content = models.TextField(
        verbose_name="Contenido",
        help_text="Texto del post en LinkedIn."
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Imagen"
    )

    link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Enlace"
    )

    scheduled_date = models.DateTimeField()

    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    panels = [
        FieldPanel("content"),
        FieldPanel("image"),
        FieldPanel("link"),
        FieldPanel("scheduled_date"),
        FieldPanel("created_by"),
    ]

    def __str__(self):
        return self.content[:50]