from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.viewsets.base import ViewSetGroup
from .models import (
    Conversation,
)

class ConversationViewSet(ModelViewSet):
    model = Conversation
    menu_label = "AI Studio Leads"
    icon = "mobile-alt"
    menu_order = 200
    add_to_admin_menu = False

    list_display = ( 
        "username",
        "phone",
        "interaction_type",
        "sentiment",
    )
    search_fields = ("created_at",)

Conversation_viewset = ConversationViewSet()

 
