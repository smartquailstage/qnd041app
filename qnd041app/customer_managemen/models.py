from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.html import format_html

# Wagtail Imports
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet
from wagtailmedia.models import Media  # Por si necesitas adjuntar multimedia en el futuro

class PlatformChoices(models.TextChoices):
    INSTAGRAM = 'instagram', 'Instagram'
    FACEBOOK = 'facebook', 'Facebook'
    WHATSAPP = 'whatsapp', 'WhatsApp'

class LeadTemperatureChoices(models.TextChoices):
    COLD = 'cold', 'Frío'
    WARM = 'warm', 'Tibio'
    HOT = 'hot', 'Caliente'

@register_snippet
class Conversation(ClusterableModel):
    """
    Modelo principal de conversación omnicanal gestionado como Snippet en Wagtail.
    Hereda de ClusterableModel para permitir la gestión de mensajes hijos mediante InlinePanel.
    """
    platform = models.CharField(
        max_length=20, 
        choices=PlatformChoices.choices,
        help_text="Plataforma de origen del mensaje"
    )
    platform_user_id = models.CharField(
        max_length=255, 
        db_index=True,
        help_text="ID único del usuario en la red social (IGSID, PSID o número de teléfono)"
    )
    contact_name = models.CharField(max_length=255, blank=True, null=True, help_text="Nombre del lead")
    
    # Calificación de la IA
    temperature = models.CharField(
        max_length=20, 
        choices=LeadTemperatureChoices.choices, 
        default=LeadTemperatureChoices.COLD,
        help_text="Temperatura del lead evaluada por la IA"
    )
    is_hot = models.BooleanField(
        default=False, 
        help_text="Campo auxiliar rápido para verificar si el lead es caliente"
    )
    
    # Automatización de Ticket
    converted_to_ticket = models.BooleanField(
        default=False, 
        help_text="Se marca en True automáticamente cuando la conversación pasa a ser un ticket"
    )
    ticket_created_at = models.DateTimeField(
        blank=True, 
        null=True, 
        help_text="Fecha y hora exacta en que se convirtió a ticket"
    )
    
    # Metadatos de control
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Configuración de los paneles de administración en Wagtail
    panels = [
        MultiFieldPanel([
            FieldPanel('platform'),
            FieldPanel('platform_user_id'),
            FieldPanel('contact_name'),
        ], heading="Información del Contacto"),
        
        MultiFieldPanel([
            FieldPanel('temperature'),
            FieldPanel('is_hot'),
            FieldPanel('converted_to_ticket'),
            FieldPanel('ticket_created_at'),
        ], heading="Estado y Conversión (IA)"),
        
        # Permite ver y administrar los mensajes de la conversación en forma de lista vertical
        InlinePanel('messages', label="Mensajes del Chat"),
    ]

    class Meta:
        verbose_name = "Conversación"
        verbose_name_plural = "Conversaciones"
        unique_together = ('platform', 'platform_user_id')

    def __str__(self):
        status = "🔥 Caliente" if self.is_hot else "Fresco"
        ticket = " [🎫 Ticket]" if self.converted_to_ticket else ""
        return f"[{self.get_platform_display()}] {self.contact_name or self.platform_user_id} - {status}{ticket}"

    def save(self, *args, **kwargs):
        # Sincronización automática del booleano 'is_hot'
        if self.temperature == LeadTemperatureChoices.HOT:
            self.is_hot = True
        else:
            self.is_hot = False
        super().save(*args, **kwargs)

    def convert_to_ticket(self):
        """Método de negocio para convertir la conversación en ticket de forma automática."""
        if not self.converted_to_ticket:
            self.converted_to_ticket = True
            self.ticket_created_at = timezone.now()
            self.save(update_fields=['converted_to_ticket', 'ticket_created_at', 'updated_at'])

    def temperature_progress_bar(self):
        """Genera una barra de progreso visual basada en la temperatura del lead."""
        mapping = {
            'cold': {'percent': 25, 'color': '#3b82f6', 'label': 'Frío'},
            'warm': {'percent': 65, 'color': '#f59e0b', 'label': 'Tibio'},
            'hot': {'percent': 100, 'color': '#ef4444', 'label': '🔥 Caliente'},
        }
        data = mapping.get(self.temperature, {'percent': 0, 'color': '#cbd5e1', 'label': self.temperature})
        
        return format_html(
            '''
            <div style="display: flex; align-items: center; gap: 8px; width: 140px;">
                <div style="flex-grow: 1; background-color: #e2e8f0; border-radius: 9999px; height: 8px; overflow: hidden;">
                    <div style="background-color: {}; width: {}%; height: 100%; border-radius: 9999px;"></div>
                </div>
                <span style="font-size: 11px; font-weight: 600; white-space: nowrap; color: #334155;">{}</span>
            </div>
            ''',
            data['color'],
            data['percent'],
            data['label']
        )
    temperature_progress_bar.short_description = "Temperatura del Lead"

    def ticket_status_indicator(self):
        """Muestra un punto intermitente (verde si está convertido, rojo si está pendiente)."""
        if self.converted_to_ticket:
            return format_html(
                '''
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="
                        height: 12px;
                        width: 12px;
                        background-color: #22c55e;
                        border-radius: 50%;
                        display: inline-block;
                        box-shadow: 0 0 0 rgba(34, 197, 94, 0.4);
                        animation: pulse-green 2s infinite;
                    "></span>
                    <span style="font-size: 12px; font-weight: 600; color: #15803d;">Convertido</span>
                </div>
                <style>
                @keyframes pulse-green {{
                    0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }}
                    70% {{ transform: scale(1); box-shadow: 0 0 0 8px rgba(34, 197, 94, 0); }}
                    100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }}
                }}
                </style>
                '''
            )
        else:
            return format_html(
                '''
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="
                        height: 12px;
                        width: 12px;
                        background-color: #ef4444;
                        border-radius: 50%;
                        display: inline-block;
                        animation: pulse-red 2s infinite;
                    "></span>
                    <span style="font-size: 12px; font-weight: 600; color: #b91c1c;">Pendiente</span>
                </div>
                <style>
                @keyframes pulse-red {{
                    0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
                    70% {{ transform: scale(1); box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }}
                    100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
                }}
                </style>
                '''
            )
    ticket_status_indicator.short_description = "Converted to ticket"


class Message(Orderable):
    """
    Modelo hijo para almacenar los mensajes individuales asociados a una conversación.
    Hereda de Orderable para mantener el orden cronológico o manual.
    """
    SENDER_CHOICES = [
        ('user', 'Usuario / Lead'),
        ('ai', 'Asistente IA'),
        ('agent', 'Agente Humano'),
    ]

    conversation = ParentalKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    sender_type = models.CharField(max_length=20, choices=SENDER_CHOICES)
    content = models.TextField(help_text="Contenido del mensaje")
    message_id = models.CharField(
        max_length=255, 
        unique=True, 
        blank=True, 
        null=True,
        help_text="ID del mensaje devuelto por la API de Meta / WhatsApp"
    )
    timestamp = models.DateTimeField(default=timezone.now)

    panels = [
        FieldPanel('sender_type'),
        FieldPanel('content'),
        FieldPanel('message_id'),
        FieldPanel('timestamp'),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"

    def __str__(self):
        return f"{self.get_sender_type_display()}: {self.content[:30]}..."