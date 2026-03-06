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

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class SocialAutomationVideo(models.Model):
    """
    Snippet para generación automática de videos empresariales
    optimizados para Instagram Reels, TikTok y YouTube Shorts.
    Diseñado para automatización con n8n + IA.
    """

    # ----------------------------------------
    # Tipo de contenido
    # ----------------------------------------
    VIDEO_TOPIC_CHOICES = [
        ("product_demo", "Demostración de producto"),
        ("tip", "Tip / Educativo"),
        ("story", "Historia / storytelling"),
        ("promotion", "Promoción / oferta"),
        ("behind_scenes", "Behind the scenes"),
        ("testimonial", "Testimonio cliente"),
        ("trend", "Trend / contenido viral"),
    ]

    topic = models.CharField(
        max_length=100,
        choices=VIDEO_TOPIC_CHOICES,
        help_text="Tipo estratégico de video"
    )

    # ----------------------------------------
    # Plataforma
    # ----------------------------------------
    PLATFORM_CHOICES = [
        ("instagram_reels", "Instagram Reels"),
        ("tiktok", "TikTok"),
        ("youtube_shorts", "YouTube Shorts"),
        ("multi_platform", "Multi plataforma"),
    ]

    platform = models.CharField(
        max_length=100,
        choices=PLATFORM_CHOICES,
        default="multi_platform"
    )

    # ----------------------------------------
    # Hook inicial (clave para viralidad)
    # ----------------------------------------
    hook = models.CharField(
        max_length=300,
        blank=True,
        help_text="Frase de apertura que captura la atención en los primeros 3 segundos"
    )

    # ----------------------------------------
    # Contexto del video
    # ----------------------------------------
    video_context = models.TextField(
        blank=True,
        help_text="Contexto del video: producto, audiencia, campaña, etc."
    )

    # ----------------------------------------
    # Guion
    # ----------------------------------------
    script = models.TextField(
        blank=True,
        help_text="Guion del video generado o editado manualmente"
    )

    # ----------------------------------------
    # Call to Action
    # ----------------------------------------
    CTA_CHOICES = [
        ("visit_website", "Visitar website"),
        ("buy_now", "Comprar ahora"),
        ("follow", "Seguir cuenta"),
        ("comment", "Comentar"),
        ("share", "Compartir"),
        ("link_bio", "Link en bio"),
    ]

    call_to_action = models.CharField(
        max_length=100,
        choices=CTA_CHOICES,
        blank=True
    )

    # ----------------------------------------
    # Duración
    # ----------------------------------------
    DURATION_CHOICES = [
        ("7s", "7 segundos"),
        ("15s", "15 segundos"),
        ("30s", "30 segundos"),
        ("45s", "45 segundos"),
        ("60s", "60 segundos"),
    ]

    duration = models.CharField(
        max_length=20,
        choices=DURATION_CHOICES,
        default="15s"
    )

    # ----------------------------------------
    # Estilo visual
    # ----------------------------------------
    STYLE_CHOICES = [
        ("cinematic", "Cinemático"),
        ("ugc", "UGC estilo usuario"),
        ("minimal", "Minimalista"),
        ("corporate", "Corporativo"),
        ("dynamic", "Dinámico / viral"),
        ("ai_generated", "AI generado"),
    ]

    style = models.CharField(
        max_length=100,
        choices=STYLE_CHOICES,
        blank=True
    )

    # ----------------------------------------
    # Mood / música
    # ----------------------------------------
    MUSIC_STYLE_CHOICES = [
        ("upbeat", "Energética"),
        ("corporate", "Corporativa"),
        ("inspirational", "Inspiracional"),
        ("trendy", "Trendy TikTok"),
        ("ambient", "Ambiental"),
    ]

    music_style = models.CharField(
        max_length=100,
        choices=MUSIC_STYLE_CHOICES,
        blank=True
    )

    # ----------------------------------------
    # Subtítulos automáticos
    # ----------------------------------------
    subtitles = models.BooleanField(
        default=True,
        help_text="Generar subtítulos automáticos"
    )

    # ----------------------------------------
    # Logo
    # ----------------------------------------
    company_logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True
    )

    # ----------------------------------------
    # Estado
    # ----------------------------------------
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("processing", "Procesando"),
        ("completed", "Completado"),
        ("error", "Error"),
    ]

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # ----------------------------------------
    # Fecha programada
    # ----------------------------------------
    scheduled_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha programada para publicación"
    )

    # ----------------------------------------
    # Resultado del video
    # ----------------------------------------
    generated_video_url = models.URLField(
        blank=True,
        null=True,
        max_length=1000,
        help_text="URL del video generado"
    )

    celery_task_id = models.CharField(
      max_length=255,
      null=True,
      blank=True,
      help_text="Track ID de la tarea programada"
    )

    # ----------------------------------------
    # Wagtail Panels
    # ----------------------------------------
    panels = [
        FieldPanel("topic"),
        FieldPanel("platform"),
        FieldPanel("hook"),
        FieldPanel("video_context"),
        FieldPanel("script"),
        FieldPanel("call_to_action"),
        FieldPanel("duration"),
        FieldPanel("style"),
        FieldPanel("music_style"),
        FieldPanel("subtitles"),
        FieldPanel("company_logo"),
        FieldPanel("scheduled_datetime"),
        FieldPanel("status"),
        FieldPanel("generated_video_url"),
        FieldPanel("celery_task_id"),
    ]

    class Meta:
        verbose_name = "AI Video Creator"
        verbose_name_plural = "AI Video Creators"
        ordering = ["-scheduled_datetime"]

    def __str__(self):
        return f"{self.topic} - {self.platform}"




@register_snippet
class SocialAutomationPost(models.Model):
    """
    Snippet para crear imágenes de marca con Gemini usando opciones predefinidas
    y soporte de logo de la empresa.
    """

    # ----------------------------------------
    # Tipo de post
    # ----------------------------------------
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

    # ----------------------------------------
    # Tono de marca
    # ----------------------------------------
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

    # ----------------------------------------
    # Estilo visual
    # ----------------------------------------
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

    # ----------------------------------------
    # Paleta de colores
    # ----------------------------------------
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
        help_text="Categoría de paleta de colores"
    )

    # ----------------------------------------
    # Tipografía
    # ----------------------------------------
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
        help_text="Tipo de tipografía"
    )

    # ----------------------------------------
    # Formato técnico de imagen
    # ----------------------------------------
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
        help_text="Formato técnico de la imagen"
    )

    # ----------------------------------------
    # NUEVO: Tipo estratégico de imagen
    # ----------------------------------------
    IMAGE_TYPE_CHOICES = [
        ("web_landing", "Web Landing Page"),
        ("instagram_carousel", "Instagram Carrusel"),
        ("instagram_post", "Instagram Post"),
        ("instagram_story", "Instagram Stories"),
    ]

    image_type = models.CharField(
        max_length=50,
        choices=IMAGE_TYPE_CHOICES,
        blank=True,
        help_text="Destino estratégico de la imagen"
    )

    # ----------------------------------------
    # NUEVO: Contexto de imagen
    # ----------------------------------------
    image_context = models.TextField(
        blank=True,
        help_text="Contexto adicional para la generación de la imagen (mensaje, campaña, audiencia, etc.)"
    )

    # ----------------------------------------
    # Textos
    # ----------------------------------------
    title_text = models.TextField(
        blank=True,
        help_text="Texto principal que aparecerá en la imagen"
    )

    brand_text = models.TextField(
        blank=True,
        help_text="Texto de la marca (slogan o mensaje)"
    )

    company_info_text = models.TextField(
        blank=True,
        help_text="Información adicional (website, descriptor, contacto)"
    )

    # ----------------------------------------
    # Logo
    # ----------------------------------------
    company_logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True,
        help_text="Logo de la empresa"
    )

    # ----------------------------------------
    # Estado
    # ----------------------------------------
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("processing", "Procesando"),
        ("completed", "Completado"),
        ("error", "Error"),
    ]

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="pending"
    )

    scheduled_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha programada para el posteo"
    )

    generated_image_url = models.URLField(
        blank=True,
        null=True,
        max_length=1000,
        help_text="URL de la imagen generada por IA"
    )

    # ----------------------------------------
    # Wagtail Panels
    # ----------------------------------------
    panels = [
        FieldPanel("title"),
        FieldPanel("brand_voice"),
        FieldPanel("style"),
        FieldPanel("color_palette"),
        FieldPanel("font_style"),
        FieldPanel("format"),
        FieldPanel("image_type"),      # NUEVO
        FieldPanel("image_context"),   # NUEVO
        FieldPanel("title_text"),
        FieldPanel("brand_text"),
        FieldPanel("company_info_text"),
        FieldPanel("company_logo"),
        FieldPanel("scheduled_datetime"),
        FieldPanel("status"),
        FieldPanel("generated_image_url"),
    ]

    class Meta:
        verbose_name = "AI Content Image Creator"
        verbose_name_plural = "AI Content Image Creators"
        ordering = ["-scheduled_datetime"]

    def __str__(self):
        return self.title or f"Brand Post #{self.id}"
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


# models.py

from django.db import models
from wagtail.models import DraftStateMixin, RevisionMixin
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string
from wagtail.search import index


@register_snippet
class AIInstagramPostPublished(DraftStateMixin, RevisionMixin, models.Model):

    # =========================
    # CHOICES
    # =========================

    POST_TYPE_CHOICES = [
        ("educational", "Educativo"),
        ("sales", "Venta"),
        ("engagement", "Engagement"),
        ("storytelling", "Storytelling"),
        ("personal_brand", "Marca Personal"),
    ]

    TONE_CHOICES = [
        ("casual", "Casual"),
        ("professional", "Profesional"),
        ("friendly", "Amigable"),
        ("authoritative", "Autoridad"),
        ("inspirational", "Inspirador"),
    ]

    OBJECTIVE_CHOICES = [
        ("increase_sales", "Aumentar ventas"),
        ("generate_leads", "Generar leads"),
        ("increase_engagement", "Aumentar engagement"),
        ("educate", "Educar audiencia"),
        ("brand_awareness", "Reconocimiento de marca"),
    ]

    STATUS_CHOICES = [
        ("draft", "Borrador"),
        ("ready", "Listo para publicar"),
        ("scheduled", "Programado"),
        ("published", "Publicado"),
    ]

    # =========================
    # INFORMACIÓN BASE
    # =========================

    title = models.CharField(max_length=255, null=True, blank=True)

    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True
    )

    post_type = models.CharField(
        max_length=50,
        choices=POST_TYPE_CHOICES,
        null=True,
        blank=True
    )

    tone = models.CharField(
        max_length=50,
        choices=TONE_CHOICES,
        null=True,
        blank=True
    )

    objective = models.CharField(
        max_length=50,
        choices=OBJECTIVE_CHOICES,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        null=True,
        blank=True
    )

    # =========================
    # CONTEXTO PARA IA
    # =========================

    ai_context = models.TextField(
        null=True,
        blank=True,
        help_text="Describe aquí todo el contexto para que la IA genere el copy."
    )

    # =========================
    # CONTENIDO GENERADO
    # =========================

    caption = models.TextField(
        null=True,
        blank=True
    )

    hashtags = models.TextField(
        null=True,
        blank=True
    )

    call_to_action = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    # =========================
    # IMAGEN
    # =========================

    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    # =========================
    # AUTOMATIZACIÓN
    # =========================

    scheduled_for = models.DateTimeField(
        null=True,
        blank=True
    )

    ai_generated = models.BooleanField(
        null=True,
        blank=True
    )

    # models.py (añadir al modelo AIInstagramPostPublished)

    celery_task_id = models.CharField(
      max_length=255,
      null=True,
      blank=True,
      help_text="Track ID de la tarea programada"
    )

    # =========================
    # WAGTAIL ADMIN PANELS
    # =========================

    panels = [

        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("slug"),
        ], heading="Información básica"),

        MultiFieldPanel([
            FieldPanel("post_type"),
            FieldPanel("tone"),
            FieldPanel("objective"),
            FieldPanel("status"),
        ], heading="Configuración estratégica"),

        MultiFieldPanel([
            FieldPanel("ai_context"),
        ], heading="Contexto para IA"),

        MultiFieldPanel([
            FieldPanel("image"),
        ], heading="Imagen del Post"),

        MultiFieldPanel([
            FieldPanel("caption"),
            FieldPanel("hashtags"),
            FieldPanel("call_to_action"),
        ], heading="Contenido Generado"),

        MultiFieldPanel([
            FieldPanel("scheduled_for"),
            FieldPanel("ai_generated"),
            FieldPanel("celery_task_id"),
        ], heading="Automatización"),
    ]

    search_fields = [
        index.SearchField("title"),
        index.SearchField("caption"),
        index.SearchField("ai_context"),
    ]

    class Meta:
        verbose_name = "AI Instagram Post Published"
        verbose_name_plural = "AI Instagram Posts Published"

    def __str__(self):
        return self.title or "AI Instagram Post"





from django.db import models
from wagtail.models import DraftStateMixin, RevisionMixin
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
from wagtail.images import get_image_model_string
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


# Modelo para imágenes del carrusel
class CarouselImage(models.Model):
    post = ParentalKey('AIInstagramCarouselPost', on_delete=models.CASCADE, related_name='carousel_images')
    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    caption = models.CharField(max_length=255, null=True, blank=True, help_text="Caption individual de la imagen")

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]

    def __str__(self):
        return f"Imagen {self.id} del carrusel"


@register_snippet
class AIInstagramCarouselPost(ClusterableModel, DraftStateMixin, RevisionMixin, models.Model):

    # =========================
    # CHOICES
    # =========================
    POST_TYPE_CHOICES = [
        ("educational", "Educativo"),
        ("sales", "Venta"),
        ("engagement", "Engagement"),
        ("storytelling", "Storytelling"),
        ("personal_brand", "Marca Personal"),
    ]

    TONE_CHOICES = [
        ("casual", "Casual"),
        ("professional", "Profesional"),
        ("friendly", "Amigable"),
        ("authoritative", "Autoridad"),
        ("inspirational", "Inspirador"),
    ]

    OBJECTIVE_CHOICES = [
        ("increase_sales", "Aumentar ventas"),
        ("generate_leads", "Generar leads"),
        ("increase_engagement", "Aumentar engagement"),
        ("educate", "Educar audiencia"),
        ("brand_awareness", "Reconocimiento de marca"),
    ]

    STATUS_CHOICES = [
        ("draft", "Borrador"),
        ("ready", "Listo para publicar"),
        ("scheduled", "Programado"),
        ("published", "Publicado"),
    ]

    # =========================
    # INFORMACIÓN BASE
    # =========================
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    post_type = models.CharField(max_length=50, choices=POST_TYPE_CHOICES, null=True, blank=True)
    tone = models.CharField(max_length=50, choices=TONE_CHOICES, null=True, blank=True)
    objective = models.CharField(max_length=50, choices=OBJECTIVE_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)

    # =========================
    # CONTEXTO PARA IA
    # =========================
    ai_context = models.TextField(
        null=True,
        blank=True,
        help_text="Describe aquí todo el contexto para generar captions, copy y hashtags del carrusel"
    )

    # =========================
    # CONTENIDO GENERADO
    # =========================
    caption = models.TextField(null=True, blank=True)
    hashtags = models.TextField(null=True, blank=True)
    call_to_action = models.CharField(max_length=255, null=True, blank=True)

    # =========================
    # AUTOMATIZACIÓN
    # =========================
    scheduled_for = models.DateTimeField(null=True, blank=True)
    ai_generated = models.BooleanField(null=True, blank=True)
    celery_task_id = models.CharField(max_length=255, null=True, blank=True)

    # =========================
    # PANEL DE ADMIN
    # =========================
    panels = [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("slug"),
        ], heading="Información básica"),

        MultiFieldPanel([
            FieldPanel("post_type"),
            FieldPanel("tone"),
            FieldPanel("objective"),
            FieldPanel("status"),
        ], heading="Configuración estratégica"),

        MultiFieldPanel([
            FieldPanel("ai_context"),
        ], heading="Contexto para IA"),

        InlinePanel("carousel_images", label="Imágenes del Carrusel", min_num=1, max_num=10),

        MultiFieldPanel([
            FieldPanel("caption"),
            FieldPanel("hashtags"),
            FieldPanel("call_to_action"),
        ], heading="Contenido Generado"),

        MultiFieldPanel([
            FieldPanel("scheduled_for"),
            FieldPanel("ai_generated"),
            FieldPanel("celery_task_id"),
        ], heading="Automatización"),
    ]

    search_fields = [
        index.SearchField("title"),
        index.SearchField("caption"),
        index.SearchField("ai_context"),
    ]

    class Meta:
        verbose_name = "AI Instagram Carousel Post"
        verbose_name_plural = "AI Instagram Carousel Posts"

    def __str__(self):
        return self.title or "AI Instagram Carousel Post"





from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail.images import get_image_model_string


@register_snippet
class AIInstagramCarouselPost(models.Model):

    # =========================
    # CHOICES
    # =========================

    POST_TYPE_CHOICES = [
        ("educational", "Educativo"),
        ("sales", "Venta"),
        ("engagement", "Engagement"),
        ("storytelling", "Storytelling"),
        ("personal_brand", "Marca Personal"),
    ]

    TONE_CHOICES = [
        ("casual", "Casual"),
        ("professional", "Profesional"),
        ("friendly", "Amigable"),
        ("authoritative", "Autoridad"),
        ("inspirational", "Inspirador"),
    ]

    VISUAL_STYLE_CHOICES = [
        ("minimalist", "Minimalista"),
        ("bold_typography", "Tipografía fuerte"),
        ("illustration", "Ilustración"),
        ("3d", "3D"),
        ("photorealistic", "Fotorealista"),
        ("flat_design", "Flat design"),
    ]

    LAYOUT_STYLE_CHOICES = [
        ("centered", "Texto centrado"),
        ("split", "Texto + imagen"),
        ("top_text", "Texto arriba"),
        ("big_number", "Número grande"),
        ("quote", "Quote layout"),
    ]

    STATUS_CHOICES = [
        ("draft", "Borrador"),
        ("ready", "Listo para generar"),
        ("generating", "Generando imágenes"),
        ("completed", "Completado"),
        ("failed", "Error"),
    ]

    # =========================
    # INFORMACIÓN BASE
    # =========================

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Nombre interno del carrusel. No aparece en las imágenes."
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
        help_text="Identificador único usado por APIs y automatizaciones."
    )

    post_type = models.CharField(
        max_length=50,
        choices=POST_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text="Tipo de contenido del carrusel."
    )

    tone = models.CharField(
        max_length=50,
        choices=TONE_CHOICES,
        blank=True,
        null=True,
        help_text="Tono del contenido generado por IA."
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="draft",
        help_text="Estado del proceso de generación."
    )

    slides_to_generate = models.IntegerField(
        default=5,
        help_text="Cantidad de slides que se generarán (1-10)."
    )

    # =========================
    # CONTEXTO PARA IA
    # =========================

    ai_context = models.TextField(
        blank=True,
        null=True,
        help_text="""
Describe el contexto del carrusel:
- tema principal
- público objetivo
- problema que se quiere explicar
- tipo de contenido (tips, errores, guía, etc.)

La IA usará este contexto para construir los prompts de imagen.
"""
    )

    visual_style = models.CharField(
        max_length=50,
        choices=VISUAL_STYLE_CHOICES,
        blank=True,
        null=True,
        help_text="Estilo visual general de las imágenes."
    )

    layout_style = models.CharField(
        max_length=50,
        choices=LAYOUT_STYLE_CHOICES,
        blank=True,
        null=True,
        help_text="Distribución del contenido dentro del slide."
    )

    # =========================
    # SLIDE 1
    # =========================

    slide1_headline = models.CharField(max_length=255, blank=True, null=True, help_text="Texto principal del slide.")
    slide1_subheadline = models.CharField(max_length=255, blank=True, null=True, help_text="Texto secundario opcional.")
    slide1_prompt = models.TextField(blank=True, null=True, help_text="Prompt visual para generar la imagen.")
    slide1_negative_prompt = models.TextField(blank=True, null=True, help_text="Elementos que la IA debe evitar.")
    slide1_image = models.ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+", help_text="Imagen generada por IA.")

    # =========================
    # SLIDE 2
    # =========================

    slide2_headline = models.CharField(max_length=255, blank=True, null=True)
    slide2_subheadline = models.CharField(max_length=255, blank=True, null=True)
    slide2_prompt = models.TextField(blank=True, null=True)
    slide2_negative_prompt = models.TextField(blank=True, null=True)
    slide2_image = models.ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    # =========================
    # SLIDE 3
    # =========================

    slide3_headline = models.CharField(max_length=255, blank=True, null=True)
    slide3_subheadline = models.CharField(max_length=255, blank=True, null=True)
    slide3_prompt = models.TextField(blank=True, null=True)
    slide3_negative_prompt = models.TextField(blank=True, null=True)
    slide3_image = models.ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    # =========================
    # SLIDE 4
    # =========================

    slide4_headline = models.CharField(max_length=255, blank=True, null=True)
    slide4_subheadline = models.CharField(max_length=255, blank=True, null=True)
    slide4_prompt = models.TextField(blank=True, null=True)
    slide4_negative_prompt = models.TextField(blank=True, null=True)
    slide4_image = models.ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    # =========================
    # SLIDE 5
    # =========================

    slide5_headline = models.CharField(max_length=255, blank=True, null=True)
    slide5_subheadline = models.CharField(max_length=255, blank=True, null=True)
    slide5_prompt = models.TextField(blank=True, null=True)
    slide5_negative_prompt = models.TextField(blank=True, null=True)
    slide5_image = models.ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    # =========================
    # SLIDE 6
    # =========================

    slide6_headline = models.CharField(max_length=255, blank=True, null=True)
    slide6_subheadline = models.CharField(max_length=255, blank=True, null=True)
    slide6_prompt = models.TextField(blank=True, null=True)
    slide6_negative_prompt = models.TextField(blank=True, null=True)
    slide6_image = models.ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    # =========================
    # SLIDE 7
    # =========================

    slide7_headline = models.CharField(max_length=255, blank=True, null=True)
    slide7_subheadline = models.CharField(max_length=255, blank=True, null=True)
    slide7_prompt = models.TextField(blank=True, null=True)
    slide7_negative_prompt = models.TextField(blank=True, null=True)
    slide7_image = models.ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    # =========================
    # SLIDE 8
    # =========================

    slide8_headline = models.CharField(max_length=255, blank=True, null=True)
    slide8_subheadline = models.CharField(max_length=255, blank=True, null=True)
    slide8_prompt = models.TextField(blank=True, null=True)
    slide8_negative_prompt = models.TextField(blank=True, null=True)
    slide8_image = models.ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    # =========================
    # SLIDE 9
    # =========================

    slide9_headline = models.CharField(max_length=255, blank=True, null=True)
    slide9_subheadline = models.CharField(max_length=255, blank=True, null=True)
    slide9_prompt = models.TextField(blank=True, null=True)
    slide9_negative_prompt = models.TextField(blank=True, null=True)
    slide9_image = models.ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    # =========================
    # SLIDE 10
    # =========================

    slide10_headline = models.CharField(max_length=255, blank=True, null=True)
    slide10_subheadline = models.CharField(max_length=255, blank=True, null=True)
    slide10_prompt = models.TextField(blank=True, null=True)
    slide10_negative_prompt = models.TextField(blank=True, null=True)
    slide10_image = models.ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    # =========================
    # AUTOMATIZACIÓN
    # =========================

    ai_generated = models.BooleanField(
        default=False,
        help_text="Indica si las imágenes ya fueron generadas."
    )

    celery_task_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="ID de tarea para procesos async."
    )

    # =========================
    # ADMIN PANELS
    # =========================

    panels = [

        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("slug"),
            ],
            heading="Información básica",
        ),

        MultiFieldPanel(
            [
                FieldPanel("post_type"),
                FieldPanel("tone"),
                FieldPanel("status"),
                FieldPanel("slides_to_generate"),
            ],
            heading="Configuración estratégica",
        ),

        MultiFieldPanel(
            [
                FieldPanel("ai_context"),
                FieldPanel("visual_style"),
                FieldPanel("layout_style"),
            ],
            heading="Contexto para IA",
        ),

        MultiFieldPanel(
            [
                FieldPanel("slide1_headline"),
                FieldPanel("slide1_subheadline"),
                FieldPanel("slide1_prompt"),
                FieldPanel("slide1_negative_prompt"),
                FieldPanel("slide1_image"),
            ],
            heading="Slide 1 — Hook",
        ),

        MultiFieldPanel(
            [
                FieldPanel("slide2_headline"),
                FieldPanel("slide2_subheadline"),
                FieldPanel("slide2_prompt"),
                FieldPanel("slide2_negative_prompt"),
                FieldPanel("slide2_image"),
            ],
            heading="Slide 2",
        ),

        MultiFieldPanel(
            [
                FieldPanel("slide3_headline"),
                FieldPanel("slide3_subheadline"),
                FieldPanel("slide3_prompt"),
                FieldPanel("slide3_negative_prompt"),
                FieldPanel("slide3_image"),
            ],
            heading="Slide 3",
        ),

    ]

    search_fields = [
        index.SearchField("title"),
        index.SearchField("ai_context"),
    ]

    class Meta:
        verbose_name = "AI Instagram Carousel"
        verbose_name_plural = "AI Instagram Carousels"

    def __str__(self):
        return self.title or "AI Instagram Carousel"