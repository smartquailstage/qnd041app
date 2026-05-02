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

    prompt = RichTextField(verbose_name="AI Agentic Instagram Post Creator",
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
    
    
    
    # ========================================================
    # VISTA PREVIA INTERACTIVA (Corregida para evitar IndexError)
    # ========================================================
    def image_thumb(self):
        post_id = self.id
        category_name = self.categories.name if self.categories else "Sin Categoría"
        url = str(self.image).strip() if self.image else None
        
        # Truncado de seguridad para no romper el diseño de la tabla
        cap_text = (self.caption[:75] + "...") if self.caption and len(self.caption) > 75 else (self.caption or "")
        copy_text = (self.copy[:50] + "...") if self.copy and len(self.copy) > 50 else (self.copy or "")
        tags_text = self.hashtags or ""

        if url:
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
                ''',
                post_id,        # {} n.0
                category_name,  # {} n.1
                url,            # {} n.2
                url,            # {} n.3
                cap_text,       # {} n.4
                copy_text,      # {} n.5
                tags_text       # {} n.6
            )
        
        return format_html(
            '<div style="font-size: 11px; color: #999;"><b>Post: N. {}</b><br>Cat: {}<br><i>(Esperando generación...)</i></div>',
            post_id,
            category_name
        )

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


class InstagramCarouselImage(Orderable):

    post = ParentalKey(
        InstagramCarouselPost,
        related_name="images",
        on_delete=models.CASCADE
    )

    caption = models.TextField(blank=True,null=True)
    copy = models.TextField(blank=True,null=True)
    hashtags = models.TextField(blank=True,null=True)

    image = models.ForeignKey(
        'wagtailimages.Image', # 👈 Debe ser la relación al modelo de imagen de Wagtail
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )s

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
        FieldPanel("copy"),
        FieldPanel("hashtags"),
    ]

# =========================
# 🔹 INSTAGRAM CAROUSEL
# =========================

class InstagramCarouselPost(ClusterableModel, BasePost):

    IMAGE_SIZE_CHOICES = [
        ('square', 'Cuadrado'),
        ('vertical', 'Vertical'),
        ('horizontal', 'Horizontal'),
        ('story', 'Story'),
    ]

    slides = models.PositiveIntegerField(
    default=1,
    verbose_name="Número de slides",
    help_text="Cantidad de imágenes/slides del carrusel"
    )

    image_size = models.CharField(
        max_length=20,
        choices=IMAGE_SIZE_CHOICES,
        null=True,
        blank=True,
        verbose_name="Formato Visual",
        help_text="Elija un formato para este carrusel"
    )

    categories = models.ForeignKey(
        CategoryItem,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Campaña",
        help_text="Elija la campaña para este carrusel"
    )

    prompt = RichTextField(
        verbose_name="AI Agentic Instagram Carousel Creator",
        help_text="Describa un contexto de acuerdo a la campaña",
        null=True,
        blank=True
    )

# ========================================================
    # 📸 VISTA PREVIA ESTILO INSTAGRAM (CORREGIDA)
    # ========================================================
    def carousel_preview(self):
        # Usamos select_related para optimizar la carga de imágenes
        slides = self.images.all().order_by('sort_order').select_related('image')
        post_id = self.id or "Nuevo"
        category_name = self.categories.name if self.categories else "Sin Categoría"
        total_previstos = self.slides or 0

        if slides.exists():
            html_slides = ""
            html_dots = ""
            
            for i, slide in enumerate(slides):
                # 🛠️ Obtención de URL optimizada
                if slide.image:
                    try:
                        # Rendition cuadrada para el carrusel
                        url = slide.image.get_rendition('fill-300x300').url
                    except:
                        url = slide.image.file.url
                else:
                    url = "https://via.placeholder.com/300?text=Procesando..."

                # Truncado de textos
                copy_short = (slide.copy[:60] + "...") if slide.copy and len(slide.copy) > 60 else (slide.copy or "")
                
                # Slide individual
                html_slides += f"""
                    <div id="slide-{self.id}-{i}" style="min-width: 100%; scroll-snap-align: center; box-sizing: border-box; padding: 0 10px;">
                        <div style="background: white; border-radius: 12px; border: 1px solid #dbdbdb; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                            <img src="{url}" style="width: 100%; aspect-ratio: 1/1; object-fit: cover; display: block;" />
                            <div style="padding: 12px; height: 70px; overflow: hidden;">
                                <b style="font-size: 11px; color: #262626;">Slide {i+1}:</b>
                                <p style="font-size: 11px; color: #444; margin: 4px 0; line-height: 1.3;">{copy_short}</p>
                            </div>
                        </div>
                    </div>
                """
                
                # Puntos indicadores
                html_dots += f"""
                    <div style="width: 6px; height: 6px; border-radius: 50%; background: {'#0095f6' if i == 0 else '#ccc'}; margin: 0 3px;"></div>
                """

            return format_html(f"""
                <div style="max-width: 320px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; padding: 0 5px;">
                        <span style="font-weight: 600; font-size: 12px; color: #262626;">{category_name}</span>
                        <span style="font-size: 11px; color: #8e8e8e;">ID: {post_id}</span>
                    </div>

                    <div style="position: relative;">
                        <div style="display: flex; overflow-x: auto; scroll-snap-type: x mandatory; scroll-behavior: smooth; -webkit-overflow-scrolling: touch; scrollbar-width: none; ms-overflow-style: none;">
                            <style>
                                div::-webkit-scrollbar {{ display: none; }} /* Oculta scrollbar en Chrome/Safari */
                            </style>
                            {html_slides}
                        </div>
                    </div>

                    <div style="display: flex; justify-content: center; align-items: center; margin-top: 12px;">
                        {html_dots}
                    </div>

                    <div style="text-align: center; margin-top: 10px; font-size: 11px; color: #8e8e8e; border-top: 1px solid #efefef; padding-top: 8px;">
                        Progreso: <b>{slides.count()}</b> de <b>{total_previstos}</b> procesados
                    </div>
                </div>
            """)

        return format_html(f"""
            <div style="padding: 30px; border: 2px dashed #dbdbdb; border-radius: 12px; text-align: center; background: #fafafa;">
                <div style="color: #8e8e8e; font-size: 12px;">
                    <span style="font-size: 24px; display: block; margin-bottom: 10px;">🤖</span>
                    <b>Esperando a SmartQuail AI...</b><br>
                    n8n está trabajando en los {total_previstos} slides.
                </div>
            </div>
        """)

    carousel_preview.short_description = "Previsualización del Contenido"
    # ========================================================
    # 🧩 PANELES ACTUALIZADOS (Agregamos la preview aquí)
    # ========================================================
    panels = [
        # 1. Agregamos la preview al principio para ver el progreso
     
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("categories", classname="col6"),
                # FieldPanel("post_type", classname="col6"), # Asegúrate que BasePost tenga post_type
                FieldPanel("slides", classname="col6"),
            ]),
            FieldRowPanel([
                FieldPanel("image_size", classname="col6"),
                FieldPanel("scheduled_date", classname="col6"),
            ]),
        ], heading="Configure su Instagram Carousel"),

        FieldPanel("prompt"),
        FieldPanel("carousel_preview"), 
    ]

    # ========================================================
    # 🧠 VALIDACIÓN
    # ========================================================
    def clean(self):
        super().clean()
        if self.pk and self.images.count() > 10:
            raise ValidationError("Máximo 10 imágenes")

    # ========================================================
    # 🧩 PANELES WAGTAIL
    # ========================================================
    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("categories", classname="col6"),
                FieldPanel("post_type", classname="col6"),
                FieldPanel("slides", classname="col6"),
            ]),

            FieldRowPanel([
                FieldPanel("image_size", classname="col6"),
                FieldPanel("scheduled_date", classname="col6"),
            ]),

        ], heading="Configure su Instagram Carousel"),

        FieldPanel("prompt"),

        InlinePanel("images", label="Slides del Carousel (máx 10)"),
    ]

    class Meta:
        ordering = ["-created_at"]

    # ========================================================
    # 👤 AUTOR AUTOMÁTICO
    # ========================================================
    def save_instance(self, request, instance, is_new):
        if is_new and not instance.created_by:
            instance.created_by = request.user
        return super().save_instance(request, instance, is_new)

    # ========================================================
    # 🏷️ STRING REPRESENTATION
    # ========================================================
    def __str__(self):
        if self.categories:
            return f"Carousel - {self.categories.name}"

        if self.prompt:
            return f"Carousel: {str(self.prompt)[:30]}..."

        return f"Instagram Carousel #{self.pk or 'Nuevo'}"





from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, HelpPanel
from wagtail.fields import RichTextField
from wagtailmedia.edit_handlers import MediaChooserPanel
from django.utils.html import format_html

# Asumo que BasePost y CategoryItem ya están importados correctamente
class InstagramReel(BasePost):
    DURATION_CHOICES = [
        (5, "5 segundos - Pruebas"),
        (7, "7 segundos - Viral (Quick Hook)"),
        (15, "15 segundos - Viral (Fast Pace)"),
        (30, "30 segundos - Tendencia (Standard)"),
        (60, "60 segundos - Promocional (Detailed)"),
        (90, "90 segundos - Promocional (Long Form)"),
    ]

    duration = models.PositiveIntegerField(
        choices=DURATION_CHOICES,
        default=15,
        verbose_name="Duración del Video",
        help_text="Duración en segundos. Los videos de 7-15s suelen tener mayor viralidad."
    )

    categories = models.ForeignKey(
        CategoryItem,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Campaña",
        help_text="Elija la campaña para este Reel" # Corregido: decía carrusel
    )

    prompt = RichTextField(
        verbose_name="AI Agentic Instagram Reel Creator", # Corregido: decía carrusel
        help_text="Describa el contexto o guion base para la IA",
        null=True,
        blank=True
    )

    # 1. Campo para Wagtail Media (Almacenamiento Local)
    # Asegúrate de tener instalado wagtailmedia
    video = models.ForeignKey(
        'wagtailmedia.Media',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Video Final"
    )

    # 2. URL de respaldo/previsualización de n8n
    generated_video_url = models.URLField(
        blank=True,
        null=True,
        max_length=1000,
        verbose_name="URL de n8n (Preview)",
        help_text="URL externa para previsualización antes del guardado físico."
    )

    caption = models.TextField(blank=True)
    copy = models.TextField(blank=True, verbose_name="Texto en Video (Copy)") # Añadido para consistencia con la Task
    hashtags = models.TextField(blank=True)


    def reel_preview(self):
        post_id = self.id or "Nuevo"
        category_name = self.categories.name if self.categories else "Sin Categoría"
        # Usamos la URL generada por n8n para la pre-visualización
        video_url = self.generated_video_url if self.generated_video_url else None
        
        # Truncado de seguridad para los textos
        cap_text = (self.caption[:75] + "...") if self.caption and len(self.caption) > 75 else (self.caption or "")
        copy_text = (self.copy[:50] + "...") if self.copy and len(self.copy) > 50 else (self.copy or "")
        tags_text = (self.hashtags[:60] + "...") if self.hashtags and len(self.hashtags) > 60 else (self.hashtags or "")

        if video_url:
            return format_html(
                '''
                <div style="width: 200px; font-family: -apple-system, sans-serif; font-size: 11px;">
                    <div style="margin-bottom: 5px; color: #666; font-weight: bold;">
                        Reel: N. {} | {}
                    </div>
                    
                    <div style="border: 1px solid #dbdbdb; border-radius: 12px; background: white; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <div style="position: relative; background: #000; width: 100%; aspect-ratio: 9/16; display: flex; align-items: center;">
                            <video style="width: 100%; height: 100%; object-fit: cover;" controls>
                                <source src="{}" type="video/mp4">
                                Tu navegador no soporta video.
                            </video>
                        </div>
                        
                        <div style="padding: 10px; line-height: 1.4;">
                            <div style="margin-bottom: 6px;">
                                <b style="color: #262626; display: block;">Caption:</b> 
                                <span style="color: #444;">{}</span>
                            </div>
                            <div style="margin-bottom: 6px; padding: 4px; background: #f8f9fa; border-radius: 4px;">
                                <b style="color: #262626;">Copy Video:</b> 
                                <span style="color: #444;">{}</span>
                            </div>
                            <div style="color: #00376b; word-break: break-all; font-size: 10px; margin-top: 4px;">
                                {}
                            </div>
                            <div style="margin-top: 8px; border-top: 1px solid #eee; padding-top: 5px;">
                                <a href="{}" target="_blank" style="color: #555; text-decoration: none; font-size: 9px;">🔗 Ver enlace directo</a>
                            </div>
                        </div>
                    </div>
                </div>
                ''',
                post_id,        # {} n.0
                category_name,  # {} n.1
                video_url,      # {} n.2 (source video)
                cap_text,       # {} n.3
                copy_text,      # {} n.4
                tags_text,      # {} n.5
                video_url       # {} n.6 (link externo)
            )
        
        return format_html(
            '<div style="font-size: 11px; color: #999; padding: 10px; border: 1px dashed #ccc; border-radius: 8px;">'
            '<b>Reel: N. {}</b><br>Cat: {}<br><i>(Esperando renderizado de video en n8n...)</i></div>',
            post_id,
            category_name
        )

    reel_preview.short_description = "Vista Previa del Reel"



    panels = [
        MultiFieldPanel([
            FieldPanel("categories"),
            FieldPanel("status"), # Asumiendo que viene de BasePost
            FieldPanel("scheduled_date"),
            FieldPanel("duration"),
        ], heading="Configuración del Reel"),
        
        FieldPanel("prompt"),

        MultiFieldPanel([
            MediaChooserPanel("video"),
        ], heading="Contenido Multimedia"),

        MultiFieldPanel([
            FieldPanel("caption"),
            FieldPanel("copy"),
            FieldPanel("hashtags"),
        ], heading="Textos de IA"),
    ]

    def __str__(self):
        # Manejo de error si categories es None
        return f"Reel - {self.categories.name}" if self.categories else f"Reel #{self.id}"

    class Meta:
        verbose_name = "Instagram Reel"
        verbose_name_plural = "Instagram Reels"
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