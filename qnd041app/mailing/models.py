from django.conf import settings
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import DraftStateMixin, RevisionMixin
from wagtail.snippets.models import register_snippet


@register_snippet
class MailingItem(DraftStateMixin, RevisionMixin, models.Model):
    TIPO_MAILING_CHOICES = [
        ("informativo", "Informativo"),
        ("comunicativo", "Comunicativo"),
        ("financiero", "Financiero"),
        ("publicitario", "Publicitario"),
        ("bienvenida", "bienvenida"),
        ("soporte", "soporte"),
    ]

    ESTADO_CHOICES = [
        ("borrador", "Borrador"),
        ("programado", "Programado / Listo para enviar"),
        ("enviado", "Enviado"),
    ]

    # Opciones de idioma solicitadas
    IDIOMA_CHOICES = [
        ("es", "Español"),
        ("en", "Inglés"),
        ("fr", "Francés"),
    ]

# Nuevo campo de idioma
    idioma = models.CharField(
        max_length=10,
        choices=IDIOMA_CHOICES,
        default="es",
        verbose_name="Idioma del Mailing",
    )

    # Relación con tu CustomUser
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Usuario Destinatario",
    )

    # Campos principales
    titulo = models.CharField(
        max_length=255, verbose_name="Título / Asunto"
    )  # Añadido para que coincida con tu __str__
    tipo_mailing = models.CharField(
        max_length=50,
        choices=TIPO_MAILING_CHOICES,
        default="informativo",
        verbose_name="Tipo de Mailing",
    )
    fecha_programada = models.DateTimeField(
        verbose_name="Fecha y Hora de Programación"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="borrador",
        verbose_name="Estado del Envío",
        help_text="Guarda como borrador o cambia a programado/enviado.",
    )
    contenido = models.TextField(
        verbose_name="Información del Mailing",
        help_text="Puedes ingresar múltiples líneas o texto enriquecido según necesites.",
    )

    # Paneles de administración para Wagtail (incluyendo 'user')
    panels = [
        FieldPanel("estado"),
        FieldPanel("user"),  # Permite seleccionar el CustomUser en Wagtail
        FieldPanel("titulo"),
        FieldPanel("idioma"),
        FieldPanel("tipo_mailing"),
        FieldPanel("fecha_programada"),
        FieldPanel("contenido"),
    ]

    def __str__(self):
        # Aquí puedes usar tanto el título como el email del usuario relacionado
        return f"{self.titulo} - Destinatario: {self.user.email} ({self.get_tipo_mailing_display()})"

    class Meta:
        verbose_name = "Mailing"
        verbose_name_plural = "Mailings"