from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel,FieldRowPanel,HelpPanel
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

    TYPE_CHOICES = [
        ("Product", "Producto"),
        ("Lunch", "Lanzamiento"),
        ("Publicitario", "Publishing"),
        ("Informativo", "info"),
    ]


    post_type = models.CharField(
        max_length=100,
        choices=TYPE_CHOICES,
        blank=True,
        help_text="Elija el tipo de post"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")

    scheduled_date = models.DateTimeField(null=True, blank=True,help_text = "Asigne una fecha y hora para publicacion automatica",verbose_name="Fecha/Hora de Publicación")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# =========================
# 🔹 INSTAGRAM POST
# =========================
class InstagramPost(BasePost):

    IMAGE_SIZE_CHOICES = [
        ('square', 'Cuadrado'),
        ('vertical', 'Vertical'),
        ('horizontal', 'Horizontal'),
        ('story', 'Story'),
    ]

    image_size = models.CharField(max_length=20, choices=IMAGE_SIZE_CHOICES,verbose_name="Formato Visual",
        help_text = "Elija un formato para este post",
        null=True, blank=True )

    categories = models.ForeignKey(
        CategoryItem,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Campaña",
        help_text = "Elija la campaña para este post" 
    )

    prompt = RichTextField(verbose_name="AI Agentic Creator",
        help_text = "Describa un contexto de acuerdo a la campaña y post", null=True, blank=True)

    caption = models.TextField(null=True, blank=True)
    copy = models.TextField(blank=True,null=True)
    hashtags = models.TextField(null=True, blank=True)

    image = models.URLField(
        blank=True,
        null=True,
        max_length=1000,
        help_text="URL de la imagen post generada por IA"
    )
    
    
    
    def image_thumb(self):
        post_id = self.id
        category_name = self.categories.name if self.categories else "Sin Categoría"
        
        if self.image:
            url = str(self.image).strip()
            caption = (self.caption[:75] + "...") if self.caption and len(self.caption) > 75 else (self.caption or "")
            copy = (self.copy[:50] + "...") if self.copy and len(self.copy) > 50 else (self.copy or "")
            hashtags = self.hashtags or ""

            return format_html(
                '''
                <div style="width: 180px; font-family: sans-serif; font-size: 11px;">
                <div style="margin-bottom: 5px; color: #666; font-weight: bold;">
                    Post: N. {} | {}
                </div>
                
                <div style="border: 1px solid #dbdbdb; border-radius: 8px; background: white; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <a href="{}" target="_blank" title="Ver imagen original" style="display: block; cursor: zoom-in;">
                        <img src="{}" style="width: 100%; aspect-ratio: 1/1; object-fit: cover; display: block;" />
                    </a>
                    
                    <div style="padding: 8px; line-height: 1.3;">
                        <div style="margin-bottom: 6px;">
                            <b style="color: #262626;">Caption:</b> 
                            <span style="color: #444;">{}</span>
                        </div>
                        <div style="margin-bottom: 6px;">
                            <b style="color: #262626;">Copy:</b> 
                            <span style="color: #444;">{}</span>
                        </div>
                        <div style="color: #00376b; word-break: break-all; font-size: 10px;">
                            {}
                        </div>
                    </div>
                </div>
            </div>
            ''',post_id, category_name, url,caption,copy,hashtags
            )
            
            return format_html(
                '<div style="font-size: 11px; color: #999;"><b>Post: N. {}</b><br>Cat: {}<br><i>(Esperando imagen...)</i></div>',
                post_id,
                category_name)

    image_thumb.short_description = "Vista Previa Post"


    panels = [
        MultiFieldPanel([
            # Estos dos campos aparecerán en la misma línea (50% cada uno)
            FieldRowPanel([
                FieldPanel("categories", classname="col6"),
                FieldPanel("post_type", classname="col6"),
                FieldPanel("image_size", classname="col6"),
                FieldPanel("scheduled_date", classname="col6"),
            ]),
        ], heading="Configure su Instagram Post"),
        
        FieldPanel("prompt"),
    ]



    class Meta:
        ordering = ["-created_at"]

    def save_instance(self, request, instance, is_new):
        if is_new and not instance.created_by:
            instance.created_by = request.user
        return super().save_instance(request, instance, is_new)
        


    def __str__(self):
        if self.categories:
            return f"Post - {self.categories.name}"
    
        if self.prompt:
            return f"Post: {str(self.prompt)[:30]}..."
        
        return f"Instagram Post #{self.pk or 'Nuevo'}"

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