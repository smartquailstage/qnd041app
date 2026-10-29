from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.viewsets.base import ViewSetGroup
from .models import Conversation, WhatsAppConversation, FacebookConversation

class ConversationViewSet(ModelViewSet):
    model = Conversation
    menu_label = "Conversaciones DM"
    icon = "comment"
    menu_order = 200
    add_to_admin_menu = False
    url_prefix = "a_conversation"
    name = "a_conversation"

    list_display = (
        "platform",
        "contact_name",
        "platform_user_id",
        "temperature_progress_bar",
        "converted_to_ticket",
        "created_at",
    )
    
    search_fields = (
        "contact_name", 
        "platform_user_id",
    )
    
    list_filter = (
        "platform", 
        "temperature", 
        "converted_to_ticket",
    )

    ordering = ("-created_at",)


class WhatsAppConversationViewSet(ModelViewSet):
    model = WhatsAppConversation
    menu_label = "Chats WhatsApp"
    icon = "phone"
    menu_order = 201
    add_to_admin_menu = False
    url_prefix = "a_whatsapp_conversation"
    name = "a_whatsapp_conversation"

    list_display = (
        "platform",
        "contact_name",
        "whatsapp_phone_number",
        "temperature_progress_bar",
        "converted_to_ticket",
        "created_at",
    )
    
    search_fields = (
        "contact_name", 
        "whatsapp_phone_number",
    )
    
    list_filter = (
        "temperature", 
        "converted_to_ticket",
    )

    ordering = ("-created_at",)


class FacebookConversationViewSet(ModelViewSet):
    model = FacebookConversation
    menu_label = "Chats Facebook"
    icon = "group"
    menu_order = 202
    add_to_admin_menu = False
    url_prefix = "a_facebook_conversation"
    name = "a_facebook_conversation"

    list_display = (
        "platform",
        "contact_name",
        "facebook_psid",
        "temperature_progress_bar",
        "converted_to_ticket",
        "created_at",
    )
    
    search_fields = (
        "contact_name", 
        "facebook_psid",
    )
    
    list_filter = (
        "temperature", 
        "converted_to_ticket",
    )

    ordering = ("-created_at",)


class OmnichannelGroup(ViewSetGroup):
    menu_label = "Gestión de Chats"
    icon = "comment"
    menu_order = 200
    items = (
        ConversationViewSet(),
        WhatsAppConversationViewSet(),
        FacebookConversationViewSet(),
    )