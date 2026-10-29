from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.viewsets.base import ViewSetGroup
from .models import Conversation, WhatsAppConversation, FacebookConversation

class ConversationViewSet(ModelViewSet):
    model = Conversation
    menu_label = "Instagram DM"
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
    menu_label = "WhatsApp DM"
    icon = "comment"
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
    menu_label = "Facebook DM"
    icon = "comment"
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
    menu_label = "Social Leads"
    icon = "comment"
    menu_order = 200
    items = (
        ConversationViewSet(),
        WhatsAppConversationViewSet(),
        FacebookConversationViewSet(),
    )