from wagtail.admin.viewsets.model import ModelViewSet
from .models import Conversation

class ConversationViewSet(ModelViewSet):
    model = Conversation
    menu_label = "Conversaciones DM"
    icon = "comment"  # Icono representativo de chat en Wagtail
    menu_order = 200
    add_to_admin_menu = True

    list_display = (
        "platform",
        "contact_name",
        "platform_user_id",
        "temperature_progress_bar",  # Barra de progreso visual de la temperatura
        "ticket_status_indicator",   # Indicador visual intermitente (Verde/Rojo) de ticket
        "created_at",
    )
    
    search_fields = (
        "contact_name", 
        "platform_user_id",
    )
    
    # Filtros laterales recomendados para control omnicanal y de IA
    list_filter = (
        "platform", 
        "temperature", 
        "converted_to_ticket",
    )

    ordering = ("-created_at",)